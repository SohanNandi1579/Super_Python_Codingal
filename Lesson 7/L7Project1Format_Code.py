s = int(input("Enter your starting number"))
e = int(input("Enter your ending number"))
myList = []
myOddList = []
myEvenList = []
for counter in range(s, e+1):
    myList.append(counter^2)


for element in myList:
    if element % 2 == 0:
        myEvenList.append(element)
    else:
        myOddList.append(element)