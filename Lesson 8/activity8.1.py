# TODO: Add two tuples together
mylist = []
tuple1 = ("default", "mode", "monitor", "keyboard", "mouse")

n= int(input("How many early christmas gifts would you like to have?: "))
for i in range(0, n):
    userinp = input("What do you want for you new tech setup?: ")
    mylist.append(userinp)

newtuple = tuple1 + tuple(mylist)
print(newtuple)
