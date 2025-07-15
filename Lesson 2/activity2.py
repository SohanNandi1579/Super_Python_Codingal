# def recursive(number: int) -> int:
#     """Recursive function for factorial.
#     :param number: Number
#     :type number: int
#     :return: Factorial
#     :rtype: int
#     """
#     holder = 1
#     while number >= 1:
#         holder = number*holder
#         number -= 1

#     return(holder)


# print(recursive(6))

# TODO: Homework: Do the same with a recursive function

def recursive(number: int) -> int:
    """Recursive function for factorial.
    :param number: Number
    :type number: int
    :return: Factorial
    :rtype: int
    """
    if number >= 2:      
        number = (number*recursive(number-1))

    return(number)


print(recursive(6))