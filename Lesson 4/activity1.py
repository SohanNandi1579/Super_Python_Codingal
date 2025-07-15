flag = 0

try:
    print("HELLO, WELCOME TO V1579 9f ChatGPT+X+")
    favourite_no = int(input("Enter your phone number here: "))
    rank = int(input("Enter your rank in your class: "))
    if len(favourite_no) == 10 and len(rank) > 3:
        flag = 1
    else:
        raise ValueError

except ValueError:
    print("You are not eligible to use ChatGPT+X+ because you don't know how to "
          "recognise numbers or your rank is not too good.")

finally:
    if flag == 1:
        print("You have gained this useful key: GhatGPT+X+")
    else:
        print("Nada")



