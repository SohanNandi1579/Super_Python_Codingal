print("Welcome to the Official Age Checker")
dictomonths = {"january": 1,} #TODO: Continue Later
age = input("Enter your age: ")
flag = 0
try:
    if type(age) == int:
        pass
    else:
        raise ValueError

    if age % 2 == 0:
        age1 = "even"
    else:
        age1 = "odd"

    flag = 1
except ValueError:
    print("The age is invalid, you may not go forward"
          "\n\tThanks for using the official age checker"
          "\n\tGovt. of all around the World.")

    flag = 0

finally:
    if flag == 1:
        print(f"Your age is {age} and it is an {age1} number!")




