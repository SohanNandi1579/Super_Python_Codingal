def checker(userInput: str, counter1: str) -> str:
    """ This function will check the value that we give with 'asker'
    :param userInput: The input that the user gives to be checked.
    :type userInput: str
    :return: Answer by telling the game if it can continue.
    :rtype: str
    """
    answer = ""
    if counter1 % 3 == 0:
        if counter1 % 3 == 0 and counter1 % 5 == 0:
            answer = ("FizzWoof")
        elif counter1 % 3 == 0 and counter1 % 4 == 0:
            answer = ("FizzBuzz")
        elif counter1 % 3 == 0 and counter1 % 4 == 0 and counter1 % 5 == 0:
            answer = ("FizzBuzzWoof")
        else:
            answer = ("Fizz")

    elif counter1 % 4 == 0:
        if counter1 % 3 == 0 and counter1 % 4 == 0:
            answer = ("FizzBuzz")
        elif counter1 % 4 == 0 and counter1 % 5 == 0:
            answer = ("BuzzWoof")
        elif counter1 % 3 == 0 and counter1 % 4 == 0 and counter1 % 5 == 0:
            answer = ("FizzBuzzWoof")
        else:
            answer = ("Buzz")

    elif counter1 % 5 == 0:
        if counter1 % 3 == 0 and counter1 % 5 == 0:
            answer = ("FizzWoof")
        elif counter1 % 4 == 0 and counter1 % 5 == 0:
            answer = ("BuzzWoof")
        elif counter1 % 3 == 0 and counter1 % 4 == 0 and counter1 % 5 == 0:
            answer = ("FizzBuzzWoof")
        else:
            answer = ("Woof")

    else:
        answer = str(counter1)

    return answer


print("Welcome to FizzBuzzWoof! Enjoy!\n")
counter = 1
while True:
    if counter % 3 == 0 and counter % 4 == 0 and counter % 5 == 0:
        print("FizzBuzzWoof")
    elif counter % 3 == 0 and counter % 4 == 0:
        print("FizzBuzz")
    elif counter % 3 == 0 and counter % 5 == 0:
        print("FizzWoof")
    elif counter % 4 == 0 and counter % 5 == 0:
        print("BuzzWoof")
    elif counter % 3 == 0:
        print("Fizz")
    elif counter % 4 == 0:
        print("Buzz")
    elif counter % 5 == 0:
        print("Woof")
    else:
        print(counter)

    counter += 1
    asker = str(input(": "))
    final = checker(asker, counter)
    if final.casefold() == asker.casefold():
        pass
    else:
        print("Sorry, you lose! Dare to play again?")
        break
    counter += 1