# # Method 1
# def detector(number: int) -> str:
#     """This function checks if the given number is odd or even.
#     :param number: The number to check.
#     :type number: int
#     :return: Odd/even
#     :rtype: str
#     """
#     if number % 2 == 0:
#         return "even"
#     else:
#         return "odd"
    

# Checker =  int(input("Enter a number: "))
# print(f" The number {Checker} is an {detector(Checker)} number.")

# Method 2
def detector(number: int) -> str:
    """This function checks if the given number is odd or even. 
    :param number: The number to check.
    :type number: int         
    :return: Odd/even
    :rtype: str
    """
    if str(number).endswith(("0", "2", "4", "6", "8")):
        return "even"
    elif str(number).endswith(("1", "3", "5", "7", "9")):
        return "odd"
    else:
        return "invalid input"


Checker =  int(input("Enter a number: "))
print(f" The number {Checker} is an {detector(Checker)} number.")