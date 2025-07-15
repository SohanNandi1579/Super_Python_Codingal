# Program to search and find 'a' in the complete program, count its occurrence and compare it with 'e'.

phrase = input("Enter a phrase: ")
number = 0

counter_a = 0
counter_e = 0

for char in phrase:
    number += 1
    if char.casefold() == "a":
        counter_a += 1
        print(f"Character 'A': No. {number} and with {counter_a} occurrences.")
        break
    elif char.casefold() == "e":
        counter_e += 1
        print(f"Character 'E': No. {number} and with {counter_e} occurrences.")
        break
    else:
        pass

