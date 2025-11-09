import random

def random_name():
    # first_names = [
    #   "Aiden", "Sophia", "Liam", "Olivia", "Noah", "Emma", "Jackson", "Ava",
    #   "Lucas", "Mia", "Ethan", "Isabella", "Mason", "Amelia", "Caden", "Harper",
    #   "Logan", "Evelyn", "Elijah", "Abigail", "James", "Emily", "Benjamin", "Ella",
    #   "Alexander", "Elizabeth", "Michael", "Camila", "Daniel", "Luna", "Henry",
    #   "Scarlett", "Sebastian", "Victoria", "Jack", "Aria", "Owen", "Grace",
    #   "Samuel", "Chloe", "Matthew", "Penelope", "Joseph", "Layla", "Levi", "Riley",
    #   "David", "Zoey", "John", "Nora"]
    # last_names =[
    #     "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    #     "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
    #     "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
    #     "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson",
    #     "Walker", "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen",
    #     "Hill", "Flores", "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera",
    #     "Campbell", "Mitchell", "Carter", "Roberts"]
    names = ["Shadowstrike", "Iron Raven", "Ghost Viper", "Cipher", "Nightfall", "Rogue Fox", "Spectre", "Hollowpoint", "Crossfire", "Phantom",
             "Zero", "Vortex", "Blackout", "Reaper", "Static", "Ashen Wolf", "Darkline", "Vector", "Nomad", "Kestrel",
             "Frostbite", "Echo", "Wraith", "Razor", "Outlaw", "Pulse", "Grimlock", "Silent Fang", "Shade", "Breaker",
             "Axel Creed", "Mara Vance", "Liam Carter", "Rhea Solis", "Julian Drake", "Marcus Vale", "Evelyn Cross", "Cole Mercer", "Niko Trent", "Adira Wren",
             "Crimson Jackal", "Gravewire", "Falcon", "Talon", "Drift", "Nocturne", "Scythe", "Blitz", "Static Wolf", "Black Thorn",
             "Vandal", "Chaser", "Hollow Vex", "Recoil", "Tracer", "Bulletstorm", "Kane Rivers", "Nadia Frost", "Ronan Pike", "Elara Quinn",
             "Spectral", "Hex", "Tempest", "Pulsefire", "Breaker Nine", "Zero Line", "Killjoy", "Skullmark", "Toxin", "Lurker",
             "Lucien Vale", "Amara Dune", "Dante Reeve", "Isla North", "Trent Myles", "Rei Axton", "Calista Vorn", "Galen Ash", "Tara Holt", "Ryder Kade",
             "Lockjaw", "Crimson Fang", "Grinder", "Duststorm", "Outreach", "Warden", "Coldlight", "Jackknife", "Static Crow", "Nomad 6",
             "Havoc", "Voltage", "Trigger", "Strayline", "Ghostline", "Falx", "Echo Hunter", "Drakon", "Prowler", "Wireframe",
             "Kade Holt", "Mira Sol", "Rowan Vale", "Dorian Pike", "Lexa Crane", "Jonas Vane", "Cora Wells", "Aiden Cross", "Nash Wren", "Iris Vale",
             "Steelbite", "Rogue Zero", "Shadowline", "Slipstream", "Null", "Obsidian", "Fangstrike", "Recoil 9", "Gravewalker", "Circuit",
             "Feral", "Sabre", "Strix", "Black Veil", "Crashline", "Specter One", "Noir", "Ghostline", "Ashmark", "Breaker 3",
             "Elior", "Krynn", "Zyraen", "Mareth", "Thalor", "Vyrra", "Elandra", "Corven", "Nirian", "Kaelis",
             "Silent Rain", "Crux", "Warden X", "Nullfire", "Ironclad", "Rogue 47", "Ghostwire", "Cipher 11", "Redline", "Vexer",
             "Juno Vale", "Talon Gray", "Mira Holt", "Lysander Quinn", "Nova Dray", "Tara Voss", "Silas Creed", "Rayne Holt", "Cass Vorn", "Jett Sol",
             "Skullbreak", "Hound", "Viper", "Driftmark", "Crossfire 7", "Outcast", "Wraithline", "Neon", "Static 8", "Talon-4",
             "Ghostlock", "Specter 6", "Silent Fang", "Vectorline", "Breaker 8", "Blackbird", "Deadshot", "Trickwire", "Hollowline", "Noctis",
             "Lyra", "Kael", "Astra", "Rowen", "Thane", "Eira", "Cassian", "Voss", "Nira", "Talonis",
             "Reaper 01", "Cipherline", "Nullstrike", "Static Fang", "Black Cross", "Warlock", "Drift 9", "Echo Line", "Lockdown", "Roguelight",
             "Raze", "Hollowfire", "Sable", "Tempest 7", "Crimson Wire", "Vandal 3", "Pulse 9", "Specterlock", "Tracer X", "Recoil 4"]
    return random.choice(names)

    # return random.choice(first_names) + " " + random.choice(last_names)

class SchoolOfCriminals:
    def __init__(self, empName, empJob, empGender, empAge, empBranch, empSalary):
        self.name = empName
        self.job = empJob
        self.gender = empGender
        self.age = empAge
        self.Branch = empBranch
        self.Salary = empSalary
        self.WantToGetKickedOut = bool(input("Please enter True or False: - 'Do You Want To Get Kicked Out?:  "))

    def confidential(self):
        self.phoneNumber = input("Please enter your Phone Number: ")
        self.address = input("Please enter your address: ")
        self.LifeChoicesHistory = input("Please enter your life choices history: ")

    # def __del__(self):
    #     print("Let's fire some employees!!!!!")
    #     print("The lucky one to get kicked out is: *DrumRoll* ")
    #     for i in range(5, -1, -1):
    #         print(f"{i}...")
    #         print("\n"* 50)
    #     print(random.choice[])

class CriminalsManagement:
    def __init__(self, empRand):
        self.empRand = random.choice[SchoolOfCriminals]
        print("Let's fire some employees!!!!!")
        print("The lucky one to get kicked out is: *DrumRoll* ")
        for i in range(5, -1, -1):
            print(f"{i}...")
            print("\n"* 50)
        print(empRand)

n = int(input("How many criminals are going to be joining the most prestigious criminal academy(PCA) this year?"))
job_offers = ["criminal"*10, "waiter"*2, "faculty"*5, "mentor"*3, "chef"*2]
gender = ["male"*10, "female"*5, "none"*1]
age = [x for x in range(0, 100)]
i = 0
while i <= n:
    l = [x for x in range(0, 9999999999999999999999999999999999999999999999999999999999999999999999999999)]
    emp_No = SchoolOfCriminals(random_name, random.choice(job_offers), random.choice(gender), random.choice(age))
    del l
