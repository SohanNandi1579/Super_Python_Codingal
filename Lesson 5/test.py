#!/usr/bin/env python3
"""
jarvis_cinematic.py

Cinematic Iron Man–style Jarvis assistant — full mode.

Key fixes & features relative to earlier attempts:
- Stable microphone calibration (calibrate once at startup; fixed energy threshold).
- Robust fallback brain that uses online dictionary (dictionaryapi.dev) and Wikipedia summaries
  when OpenAI is missing or its quota is exceeded.
- Clear command parsing: open chrome, open youtube, search, meaningof, set reminder, list reminders,
  play music (folder), run shell (restricted), status, exit.
- Non-blocking command execution (threads) and background reminder thread.
- TTS with pyttsx3, attempts to choose a British-sounding voice.
- Personality via a system prompt for OpenAI if available, and canned witty lines otherwise.
- Logging and persistent memory/history.
- Retry logic for OpenAI calls.

Author: assistant (adapted for Sohan)
Date: 2025-08-12
"""

import os
import sys
import time
import json
import queue
import threading
import subprocess
import traceback
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional, Any, Dict, List
from urllib.parse import quote_plus

# Third-party imports with helpful messages if missing
try:
    import speech_recognition as sr
except Exception as e:
    print("Missing dependency: speech_recognition. Install via: pip install SpeechRecognition")
    raise

try:
    import pyttsx3
except Exception as e:
    print("Missing dependency: pyttsx3. Install via: pip install pyttsx3")
    raise

try:
    import requests
except Exception as e:
    print("Missing dependency: requests. Install via: pip install requests")
    raise

# optional but recommended
try:
    import psutil
except Exception:
    psutil = None

try:
    import simpleaudio as sa
except Exception:
    sa = None

# OpenAI modern client (optional)
try:
    from openai import OpenAI
except Exception:
    OpenAI = None

# ---------------- CONFIG ----------------
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")  # or paste your key here
WAKE_WORD = "jarvis"
VOICE_HINT = "english"   # hint for British/english voice selection
MEMORY_FILE = Path("jarvis_memory.json")
HISTORY_FILE = Path("jarvis_history.json")
LOG_FILE = Path("jarvis_cinematic.log")
REMINDERS_KEY = "reminders"

OPENAI_MODEL = "gpt-4o-mini"
MAX_OPENAI_RETRIES = 3
OPENAI_RETRY_INITIAL_DELAY = 1.0
OPENAI_RETRY_BACKOFF = 2.0

SPEECH_RATE = 165
SPEAK_CHUNK_DELAY = 0.18

# Microphone calibration — calibrate ONCE at startup for stable energy threshold
CALIBRATE_SECONDS = 1.2
DEFAULT_ENERGY_THRESHOLD = 300  # used if calibration fails or when fixed_threshold True
FIXED_ENERGY_THRESHOLD = True   # if True, use DEFAULT_ENERGY_THRESHOLD after calibration

# microphone listen timeouts
MIC_TIMEOUT = 5
PHRASE_TIME_LIMIT = 8

# Personality prompt used if OpenAI is available
PERSONA_PROMPT = (
    "You are Jarvis, a polite, witty, and efficient British AI assistant. "
    "Answer concisely and helpfully. Address the user as 'sir' unless told otherwise. "
    "Add a short dry witty aside occasionally. Do not pretend to be human."
)

# Fallback canned lines if OpenAI is not available
FALLBACKS = {
    "greeting": "Jarvis at your service, sir.",
    "name": "You may call me Jarvis, sir.",
    "status": "All systems nominal. Power distribution stable."
}

# Dictionary & Wikipedia endpoints (fallback)
DICTIONARY_API = "https://api.dictionaryapi.dev/api/v2/entries/en/"
WIKI_SUMMARY_API = "https://en.wikipedia.org/api/rest_v1/page/summary/"

# Safety: restrict potentially dangerous shell commands unless explicit "run shell: confirm <key>"
SHELL_COMMAND_CONFIRM_KEY = "confirm-run"

# -------------- Utilities & Logging --------------
def utcnow_iso():
    return datetime.now(timezone.utc).isoformat()

def log(*parts):
    line = f"[{utcnow_iso()}] " + " ".join(str(p) for p in parts)
    print(line)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass

def safe_load(path: Path, default):
    try:
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        log("Failed reading", path, e)
    return default

def safe_write(path: Path, obj):
    try:
        path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception as e:
        log("Failed writing", path, e)

# -------------- Memory & History --------------
class Memory:
    def __init__(self, memory_file: Path, history_file: Path):
        self.mem_file = memory_file
        self.hist_file = history_file
        self.lock = threading.Lock()
        self.data = safe_load(self.mem_file, {"facts": {}, "preferences": {}, REMINDERS_KEY: []})
        self.history = safe_load(self.hist_file, [])
        log("Memory loaded. facts:", len(self.data.get("facts", {})), "history:", len(self.history))

    def save(self):
        with self.lock:
            safe_write(self.mem_file, self.data)
            safe_write(self.hist_file, self.history)

    def add_fact(self, key: str, value: Any):
        with self.lock:
            self.data.setdefault("facts", {})[key] = {"value": value, "time": utcnow_iso()}
            self.save()
            log("Saved fact", key)

    def get_fact(self, key: str):
        return self.data.get("facts", {}).get(key, {}).get("value")

    def add_reminder(self, dt_iso: str, message: str):
        with self.lock:
            self.data.setdefault(REMINDERS_KEY, []).append({"time": dt_iso, "message": message})
            self.save()
            log("Added reminder", dt_iso, message)

    def list_reminders(self):
        return list(self.data.get(REMINDERS_KEY, []))

    def pop_due_reminders(self):
        now = datetime.now(timezone.utc)
        due = []
        remaining = []
        for r in self.data.get(REMINDERS_KEY, []):
            try:
                t = datetime.fromisoformat(r["time"])
                if t <= now:
                    due.append(r)
                else:
                    remaining.append(r)
            except Exception:
                remaining.append(r)
        if len(due) > 0:
            with self.lock:
                self.data[REMINDERS_KEY] = remaining
                self.save()
        return due

    def append_history(self, prompt: str, response: str):
        with self.lock:
            self.history.append({"time": utcnow_iso(), "prompt": prompt, "response": response})
            self.history = self.history[-400:]
            self.save()

memory = Memory(MEMORY_FILE, HISTORY_FILE)

# -------------- TTS (pyttsx3) --------------
class Speaker:
    def __init__(self, rate=SPEECH_RATE, voice_hint=VOICE_HINT):
        self.engine = pyttsx3.init()
        try:
            self.engine.setProperty("rate", rate)
        except Exception as e:
            log("Could not set speech rate:", e)
        self.select_voice(voice_hint)
        self.q = queue.Queue()
        self._start_worker()
        log("TTS initialized; voice hint:", voice_hint)

    def select_voice(self, hint):
        try:
            voices = self.engine.getProperty("voices")
            chosen = None
            for v in voices:
                name = (v.name + " " + (v.id or "")).lower()
                if hint and hint in name:
                    chosen = v
                    break
            if not chosen:
                for v in voices:
                    if "english" in v.name.lower() or "british" in v.name.lower() or "uk" in v.name.lower():
                        chosen = v
                        break
            if not chosen and voices:
                chosen = voices[0]
            if chosen:
                self.engine.setProperty("voice", chosen.id)
                log("Selected voice:", chosen.name)
        except Exception as e:
            log("Voice selection failed:", e)

    def _start_worker(self):
        def worker():
            while True:
                item = self.q.get()
                if item is None:
                    break
                text, block = item
                try:
                    self.engine.say(text)
                    self.engine.runAndWait()
                except Exception as e:
                    log("TTS speak error:", e)
                finally:
                    self.q.task_done()
        t = threading.Thread(target=worker, daemon=True)
        t.start()

    def speak(self, text: str, block: bool = False):
        if not text:
            return
        self.q.put((text, block))
        if block:
            self.q.join()

    def stop(self):
        try:
            self.q.put(None)
        except Exception:
            pass

speaker = Speaker()

# -------------- Listener (stable calibration at startup) --------------
class StableListener:
    def __init__(self, calibrate_seconds=CALIBRATE_SECONDS, default_threshold=DEFAULT_ENERGY_THRESHOLD, fixed_threshold=FIXED_ENERGY_THRESHOLD):
        self.rec = sr.Recognizer()
        self.rec.dynamic_energy_threshold = False  # we will use fixed threshold after calibrate
        self.calibrated = False
        self.calibrate_seconds = calibrate_seconds
        self.default_threshold = default_threshold
        self.fixed_threshold = fixed_threshold
        self._calibrate_once()

    def _calibrate_once(self):
        # calibrate microphone ambient noise once at startup
        try:
            with sr.Microphone() as source:
                log("Calibrating microphone ambient noise for", self.calibrate_seconds, "s ...")
                self.rec.adjust_for_ambient_noise(source, duration=self.calibrate_seconds)
                cal = self.rec.energy_threshold
                log("Calibration done. measured energy_threshold:", cal)
                if self.fixed_threshold:
                    # choose default instead of variable threshold to reduce instability across runs
                    self.rec.energy_threshold = max(self.default_threshold, int(cal))
                    log("Using fixed energy_threshold:", self.rec.energy_threshold)
                self.calibrated = True
        except Exception as e:
            log("Calibration failed:", e)
            # fallback to default threshold
            self.rec.energy_threshold = self.default_threshold
            log("Using default energy_threshold:", self.default_threshold)
            self.calibrated = True

    def listen(self, timeout=MIC_TIMEOUT, phrase_time_limit=PHRASE_TIME_LIMIT) -> str:
        with sr.Microphone() as source:
            try:
                # not recalibrating here — stable threshold
                print("Listening...")
                audio = self.rec.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            except sr.WaitTimeoutError:
                log("Listen timeout — no speech detected.")
                return ""
        try:
            text = self.rec.recognize_google(audio)
            log("Recognized:", text)
            return text.strip()
        except sr.UnknownValueError:
            log("Speech was detected but could not be understood.")
            return ""
        except sr.RequestError as e:
            log("Speech recognition request error:", e)
            speaker.speak("Speech recognition service is currently unavailable.")
            return ""

listener = StableListener()

# ------------------- OpenAI Client wrapper + fallback -------------------
class AIWrapper:
    def __init__(self, api_key: str = "", model: str = OPENAI_MODEL, persona: str = PERSONA_PROMPT):
        self.api_key = api_key
        self.model = model
        self.persona = persona
        self.client = None
        if api_key and OpenAI is not None:
            try:
                self.client = OpenAI(api_key=api_key)
                log("OpenAI client initialized.")
            except Exception as e:
                log("OpenAI init failed:", e)
                self.client = None
        else:
            log("No OpenAI key or client; running fallback brain.")

    def chat(self, prompt: str, context: Optional[List[Dict]] = None) -> str:
        """
        Ask OpenAI for a reply. If not available or error, use fallback brain functions:
        1. If prompt asks 'meaning of X' -> use dictionary lookup
        2. If prompt asks general query -> use Wikipedia summary
        3. Otherwise canned fallback
        """
        if self.client is None:
            log("OpenAI client missing -> using fallback for prompt:", prompt[:120])
            return self.fallback(prompt)

        # Build messages
        messages = [{"role": "system", "content": self.persona}]
        if context:
            messages.extend(context)
        messages.append({"role": "user", "content": prompt})

        attempt = 0
        delay = OPENAI_RETRY_INITIAL_DELAY
        while attempt < MAX_OPENAI_RETRIES:
            attempt += 1
            try:
                log(f"OpenAI: sending request (attempt {attempt})...")
                resp = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    max_tokens=600
                )
                # response form: resp.choices[0].message.content
                reply = getattr(resp.choices[0].message, "content", "")
                reply = (reply or "").strip()
                log("OpenAI replied (len=%d)" % len(reply))
                return reply
            except Exception as e:
                log("OpenAI error:", e)
                s = str(e).lower()
                # if quota or auth error, break early and fallback
                if "quota" in s or "insufficient" in s or "401" in s or "invalid" in s:
                    log("Detected quota/auth issue; will fallback after retries.")
                time.sleep(delay)
                delay *= OPENAI_RETRY_BACKOFF
        log("OpenAI failed all retries; using fallback.")
        return self.fallback(prompt)

    def fallback(self, prompt: str) -> str:
        pl = prompt.lower().strip()
        # meaning of X -> dictionary
        if "meaning of" in pl or pl.startswith("meaning ") or pl.startswith("define "):
            # extract word (last token or after 'meaning of')
            word = None
            if "meaning of" in pl:
                word = pl.split("meaning of", 1)[1].strip()
            elif pl.startswith("meaning "):
                word = pl.split("meaning ", 1)[1].strip()
            elif pl.startswith("define "):
                word = pl.split("define ", 1)[1].strip()
            if word:
                defn = fetch_dictionary_definition(word)
                if defn:
                    return defn
            return "I couldn't find a dictionary entry for that. I can open a web search instead."

        # quick Wikipedia lookup: if question contains "who is", "what is", or seems informational
        if any(k in pl for k in ["who is", "what is", "tell me about", "information on", "about "]):
            # attempt to extract short topic
            topic = pl
            for prefix in ("who is", "what is", "tell me about", "information on", "about"):
                if topic.startswith(prefix):
                    topic = topic.replace(prefix, "", 1).strip()
                    break
            if topic:
                summary = fetch_wikipedia_summary(topic)
                if summary:
                    return summary
            return "I couldn't find a Wikipedia summary for that topic."

        # remember that X is Y
        if pl.startswith("remember that"):
            # format: remember that <key> is <value>
            rest = pl[len("remember that"):].strip()
            if " is " in rest:
                k, v = rest.split(" is ", 1)
                memory.add_fact(k.strip(), v.strip())
                return f"Noted: {k.strip()} is {v.strip()}."
            else:
                return "Please state it as 'remember that <thing> is <value>'."

        # small talk
        if any(k in pl for k in ["your name", "who are you"]):
            return FALLBACKS["name"]

        if any(k in pl for k in ["status", "systems", "system status"]):
            return FALLBACKS["status"]

        # generic fallback
        return FALLBACKS["greeting"]

ai = AIWrapper(api_key=OPENAI_API_KEY, model=OPENAI_MODEL, persona=PERSONA_PROMPT)

# ------------------ Network-based helpers (dictionary, wiki) ------------------
def fetch_dictionary_definition(word: str) -> Optional[str]:
    """Attempt dictionary lookup using dictionaryapi.dev (free)."""
    w = word.strip().split()[0]  # single token
    try:
        url = DICTIONARY_API + quote_plus(w)
        r = requests.get(url, timeout=6)
        if r.status_code == 200:
            data = r.json()
            if isinstance(data, list) and data:
                # take first meaning & first definition
                meanings = data[0].get("meanings", [])
                if meanings:
                    defs = meanings[0].get("definitions", [])
                    if defs:
                        definition = defs[0].get("definition", "")
                        example = defs[0].get("example")
                        resp = f"{w}: {definition}"
                        if example:
                            resp += f" — e.g., {example}"
                        return resp
        else:
            log("Dictionary API status", r.status_code)
    except Exception as e:
        log("Dictionary lookup failed:", e)
    return None

def fetch_wikipedia_summary(topic: str) -> Optional[str]:
    """Fetch short Wikipedia summary using REST API."""
    t = topic.strip().replace(" ", "_")
    try:
        url = WIKI_SUMMARY_API + quote_plus(t)
        r = requests.get(url, timeout=6, headers={"User-Agent": "JarvisCinematic/1.0"})
        if r.status_code == 200:
            data = r.json()
            extract = data.get("extract")
            if extract:
                # trim to ~400 chars
                return extract if len(extract) < 800 else extract[:800] + "..."
        else:
            log("Wikipedia status", r.status_code)
    except Exception as e:
        log("Wikipedia fetch failed:", e)
    return None

# ------------------ Command handlers ------------------
def open_youtube(_args: str = ""):
    speaker.speak("Opening YouTube, sir.")
    open_url("https://www.youtube.com")

def open_chrome(_args: str = ""):
    speaker.speak("Opening Chrome, sir.")
    # Try to open Chrome specifically; fall back to default browser
    try:
        if sys.platform.startswith("win"):
            # Common path: use 'start chrome' shell command
            subprocess.Popen(["start", "chrome"], shell=True)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", "-a", "Google Chrome"])
        else:
            # linux: try google-chrome, google-chrome-stable, or default browser
            for cmd in (["google-chrome"], ["google-chrome-stable"], ["chrome"], ["xdg-open", "https://www.google.com"]):
                try:
                    subprocess.Popen(cmd)
                    break
                except Exception:
                    continue
    except Exception as e:
        log("open_chrome error:", e)
        open_url("https://www.google.com")

def search_web(args: str):
    if not args:
        speaker.speak("What should I search for, sir?")
        return
    speaker.speak(f"Searching for {args}, sir.")
    q = quote_plus(args)
    open_url(f"https://www.google.com/search?q={q}")

def meaning_of(args: str):
    if not args:
        speaker.speak("Which word would you like the meaning of, sir?")
        return
    word = args.strip().split()[0]
    speaker.speak(f"Searching dictionary for {word}.")
    defn = fetch_dictionary_definition(word)
    if defn:
        speaker.speak(defn)
    else:
        # fallback to web search
        speaker.speak("I couldn't find a dictionary definition locally. I'll search the web, sir.")
        search_web(f"meaning of {word}")

def set_reminder(args: str):
    # expect args: "HH:MM message..." or natural language different handling
    if not args:
        speaker.speak("Please tell me the time and message, sir. Example: set reminder 18:00 Call mom.")
        return
    parts = args.strip().split(maxsplit=1)
    timepart = parts[0]
    message = parts[1] if len(parts) > 1 else "Reminder"
    try:
        dt_local_time = datetime.strptime(timepart, "%H:%M").time()
        today = datetime.now()
        candidate = datetime.combine(today.date(), dt_local_time)
        if candidate < today:
            candidate += timedelta(days=1)
        # store UTC iso
        candidate_utc = candidate.astimezone(timezone.utc)
        memory.add_reminder(candidate_utc.isoformat(), message)
        speaker.speak(f"Reminder set for {timepart}: {message}")
    except Exception:
        speaker.speak("Time format not recognized. Use HH:MM in 24-hour format, sir.")

def list_reminders(_args: str = ""):
    rems = memory.list_reminders()
    if not rems:
        speaker.speak("You have no reminders, sir.")
        return
    speaker.speak("Here are your reminders, sir.")
    for r in rems:
        try:
            t = datetime.fromisoformat(r["time"])
            localt = t.astimezone().strftime("%Y-%m-%d %H:%M")
            speaker.speak(f"At {localt}: {r.get('message')}")
        except Exception:
            speaker.speak(f"At {r.get('time')}: {r.get('message')}")

def play_music(args: str):
    if not args:
        speaker.speak("Which folder should I play from, sir? Example: play music C:\\Music")
        return
    folder = args.strip().strip('"')
    p = Path(folder)
    if not p.exists() or not p.is_dir():
        speaker.speak("Folder not found, sir.")
        return
    # find audio files
    files = [f for f in p.iterdir() if f.suffix.lower() in (".mp3", ".wav", ".ogg")]
    if not files:
        speaker.speak("No playable audio files found in that folder, sir.")
        return
    chosen = str(files[0])
    speaker.speak(f"Playing {files[0].name}, sir.")
    try:
        if chosen.lower().endswith(".wav") and sa:
            wave = sa.WaveObject.from_wave_file(chosen)
            wave.play()
        else:
            if sys.platform.startswith("win"):
                os.startfile(chosen)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", chosen])
            else:
                subprocess.Popen(["xdg-open", chosen])
    except Exception as e:
        log("play_music error:", e)
        speaker.speak("Playback failed, sir.")

def run_shell(args: str):
    """
    Very restricted shell runner. For safety, require the special confirm key.
    Usage: run shell confirm-run <your command...>
    """
    if not args:
        speaker.speak("Which command should I run, sir?")
        return
    parts = args.split(maxsplit=1)
    if parts[0] != SHELL_COMMAND_CONFIRM_KEY:
        speaker.speak("For safety, to run shell commands you must prefix with 'confirm-run'.")
        return
    if len(parts) < 2:
        speaker.speak("Please provide the command after the confirmation key, sir.")
        return
    cmd = parts[1]
    speaker.speak("Running requested command, sir. Output will be limited.")
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=12)
        out = (res.stdout or res.stderr or "(no output)").strip()
        speaker.speak(out[:400])
    except Exception as e:
        log("run_shell error:", e)
        speaker.speak("Command failed or timed out, sir.")

def system_status(_args: str = ""):
    if psutil:
        cpu = psutil.cpu_percent(interval=0.5)
        mem = int(psutil.virtual_memory().percent)
        speaker.speak(f"CPU at {int(cpu)} percent. Memory usage {mem} percent.")
    else:
        speaker.speak("System stats are limited without psutil. Install psutil for more details, sir.")

def open_url(url: str):
    try:
        import webbrowser
        webbrowser.open(url)
    except Exception as e:
        log("open_url failed:", e)
        speaker.speak("I could not open the browser, sir.")

# Command dispatch map
COMMANDS = {
    "open youtube": open_youtube,
    "open chrome": open_chrome,
    "open": lambda s: open_chrome(s),
    "search": search_web,
    "meaning of": meaning_of,
    "define": meaning_of,
    "set reminder": set_reminder,
    "list reminders": list_reminders,
    "show reminders": list_reminders,
    "play music": play_music,
    "play": play_music,
    "run shell": run_shell,
    "status": system_status,
    "exit": lambda _s: _exit_gracefully()
}

# -------------- Command parsing --------------
def parse_user_command(text: str) -> Dict[str, Any]:
    """
    Return a dict describing whether it's a command or an AI prompt.
    Uses wake-word removal and pattern matching.
    """
    t = text.strip()
    low = t.lower()

    # remove wake word if present
    if low.startswith(WAKE_WORD + ",") or low.startswith(WAKE_WORD + " "):
        low = low.replace(WAKE_WORD + ",", "").replace(WAKE_WORD + " ", "", 1).strip()
    # exact command keys (prefer longer matches)
    for key in sorted(COMMANDS.keys(), key=lambda k: -len(k)):
        if low.startswith(key):
            args = low[len(key):].strip()
            return {"type": "command", "key": key, "args": args, "orig": t}
    # check natural language patterns
    if low.startswith("meaning of ") or low.startswith("define "):
        rest = low.split(None, 2)[-1] if len(low.split())>=2 else ""
        return {"type": "command", "key": "meaning of", "args": rest, "orig": t}
    if low.startswith("search for ") or low.startswith("search "):
        # normalize to "search"
        args = low.split(None, 1)[1] if len(low.split())>1 else ""
        return {"type": "command", "key": "search", "args": args, "orig": t}
    # if short (<=3 words) treat as possible command
    tokens = low.split()
    if len(tokens) <= 3:
        # try to match first word to command map keys
        first = tokens[0] if tokens else ""
        for key in COMMANDS:
            if key.split()[0] == first:
                args = " ".join(tokens[1:]) if len(tokens) > 1 else ""
                return {"type": "command", "key": key, "args": args, "orig": t}
    # otherwise treat as AI/lookup prompt
    return {"type": "ai", "prompt": t}

# -------------- Reminder background worker --------------
def reminder_worker():
    while True:
        try:
            due = memory.pop_due_reminders()
            for r in due:
                speaker.speak(f"Reminder: {r.get('message')}")
        except Exception as e:
            log("Reminder worker exception:", e)
        time.sleep(20)

_reminder_thread = threading.Thread(target=reminder_worker, daemon=True)
_reminder_thread.start()

# -------------- Exit helper --------------
def _exit_gracefully():
    speaker.speak("Shutting down. Goodbye, sir.")
    time.sleep(0.3)
    try:
        speaker.stop()
    except Exception:
        pass
    sys.exit(0)

# -------------- Main handlers --------------
def handle_command(cmddict: Dict[str, Any]):
    try:
        k = cmddict.get("key")
        args = cmddict.get("args", "")
        handler = COMMANDS.get(k)
        if handler:
            handler(args)
        else:
            # fallback to AI interpretation
            speaker.speak("I don't have a direct command for that. Interpreting it as a request, sir.")
            handle_ai(cmddict.get("orig", cmddict.get("args", "")))
    except Exception as e:
        log("handle_command exception:", e)
        speaker.speak("I encountered an error while executing that command, sir.")

def handle_ai(prompt: str):
    speaker.speak("Working on that, sir.")
    # create context from recent history
    recent = memory.history[-6:] if memory.history else []
    context = []
    for h in recent:
        context.append({"role": "user", "content": h.get("prompt", "")})
        context.append({"role": "assistant", "content": h.get("response", "")})
    reply = ai.chat(prompt, context=context)
    memory.append_history(prompt, reply)
    # chunk and speak
    chunks = chunk_text(reply)
    for c in chunks:
        speaker.speak(c)
        time.sleep(SPEAK_CHUNK_DELAY)

def chunk_text(text: str, max_len: int = 180):
    import re
    pieces = re.split(r'(?<=[\.\?\!])\s+', text.strip())
    out = []
    cur = ""
    for p in pieces:
        if len(cur) + len(p) + 1 > max_len:
            if cur:
                out.append(cur.strip())
            cur = p
        else:
            cur = (cur + " " + p).strip() if cur else p
    if cur:
        out.append(cur.strip())
    if not out:
        return [text[:max_len]]
    return out

# -------------- Startup cinematic --------------
def startup_cinematic():
    # optional sound: place a 'startup.wav' next to script if you want
    try:
        speaker.speak("Initialization sequence started.")
        speaker.speak("Loading modules. Systems nominal.")
        if ai.client:
            speaker.speak("Cloud brain responsive. Full capabilities online.")
        else:
            if OPENAI_API_KEY:
                speaker.speak("Cloud brain present but failed to initialize. Operating in fallback mode.")
            else:
                speaker.speak("Cloud brain not configured. Operating in fallback mode.")
    except Exception as e:
        log("startup cinematic error:", e)

# -------------- Main loop --------------
def main_loop():
    startup_cinematic()
    speaker.speak("Jarvis online. Awaiting your command, sir.")
    no_speech_count = 0
    try:
        while True:
            text = listener.listen(timeout=MIC_TIMEOUT, phrase_time_limit=PHRASE_TIME_LIMIT)
            if not text:
                no_speech_count += 1
                if no_speech_count >= 6:
                    speaker.speak("Still here, sir.")
                    no_speech_count = 0
                continue
            no_speech_count = 0
            parsed = parse_user_command(text)
            if parsed["type"] == "command":
                # run command in background thread to avoid blocking mic
                t = threading.Thread(target=handle_command, args=(parsed,), daemon=True)
                t.start()
            else:
                # AI prompt: require wake word for long prompts for safety (prevent accidental cloud calls)
                if WAKE_WORD not in text.lower() and len(text.split()) > 6:
                    speaker.speak("If you'd like me to answer that, please say 'Jarvis' before your question, sir.")
                    continue
                t = threading.Thread(target=handle_ai, args=(parsed["prompt"],), daemon=True)
                t.start()
    except KeyboardInterrupt:
        _exit_gracefully()
    except SystemExit:
        raise
    except Exception as e:
        log("Main loop fatal:", e, traceback.format_exc())
        speaker.speak("A fatal error occurred. Check the logs, sir.")
        sys.exit(1)

# -------------- Initialize AI wrapper --------------
ai = AIWrapper(api_key=OPENAI_API_KEY, model=OPENAI_MODEL, persona=PERSONA_PROMPT)

# -------------- Run --------------
if __name__ == "__main__":
    log("Starting Jarvis Cinematic")
    main_loop()
