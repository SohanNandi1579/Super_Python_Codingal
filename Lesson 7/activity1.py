# Welcome to the Reversed Program
myList = []
n = int(input("No. of elements you want to add to your list: "))
for adder in range(0, n):
    addto = int(input("Enter number to add: "))
    myList.append(addto)

print(myList, list(reversed(myList)))