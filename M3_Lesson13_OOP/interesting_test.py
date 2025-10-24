# print("Hello World!")
# qsjou("Ifmmp Xpsme@")


def letter_changer(letter):
    if letter == "q":
        return "p"
    if letter == "s":
        return "r"
    if letter == "j":
        return "i"
    if letter == "o":
        return "n"
    if letter == "u":
        return "t"
    if letter == "I":
        return "H"
    if letter == "f":
        return "e"
    if letter == "m":
        return "l"
    if letter == "p":
        return "o"
    if letter == "X":
        return "W"
    if letter == "p":
        return "o"
    if letter == "s":
        return "r"
    if letter == "e":
        return "d"
    if letter == "@":
        return "!"
    else:
        return letter


stringy = None

for letter in ("""qsjou("Ifmmp Xpsme@")"""):
    stringy += (letter_changer(letter))


with open(stringy.txt, "w"):

print(stringy)

