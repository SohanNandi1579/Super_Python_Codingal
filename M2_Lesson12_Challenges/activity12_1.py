import random
from os import system

MyBoard="""
-------------
| . | o | . |
-------------
| . | . | . |
-------------
| . | X | . |
-------------"""

def check_winner(board: list) -> bool:
    """
    Checks if there is a winner.
    :param board: The board to be checked on.
    :return: True if there is a winner, False if there is not.
    """
    if board[0] == board[1] == board[2] or board[3] == board[4] == board[5] or board[6] == board[7] == board[8] or board[0] == board[3] == board[6] or board[1] == board[4] == board[7] or board[2] == board[5] == board[8] or board[0] == board[4] == board[8] or board[2] == board[4] == board[6]:
        return True


s = random.random()
chooser = random.choice(["aics", "user"])
originalBoard = ["topleft", "topmiddle", "topright", "middleleft", "middlemiddle", "middleright", "bottomleft", "bottommiddle", "bottomright"]

orBoard2 = [".",".",".",".",".",".",".",".",".",]

def listtoboard(myList: list) -> list:
    system("clear")
    """
    Gives list out.
    :param myList: the list to be edited on.
    :return: The new list in the new style
    """
    return (f"""
-------------
| {myList[0]} | {myList[1]} | {myList[2]} |
-------------
| {myList[3]} | {myList[4]} | {myList[5]} |
-------------
| {myList[6]} | {myList[7]} | {myList[8]} |
-------------""")

print(listtoboard(orBoard2))


system("clear")
print(listtoboard(originalBoard))
choice = [x for x in range(0, 9)]

print("Let's play: ")
if chooser == "aics":
    while True:
        print("My Turn First")
        piece = random.choice(choice)
        orBoard2[piece] = "0"
        print(listtoboard(orBoard2))
        choice.remove(piece)
        if check_winner(orBoard2):
            win="AI"

        enter_user = input(f"{listtoboard(orBoard2)}\n\nHere, enter which position you want in exactly the same format as the board is written: ")
        position = originalBoard.index(enter_user.replace(" ", "").casefold())
        choice.remove(position)
        orBoard2[position] = "X"
        print(listtoboard((orBoard2)))
        if check_winner(orBoard2):
            win = "HUMAN"

else:
    while True:
        print("Your Turn First!")
        enter_user = input(f"{listtoboard(orBoard2)}\n\nHere, enter which position you want in exactly the same format as the board is written: ")
        position = originalBoard.index(enter_user.replace(" ", "").casefold())
        choice.remove(position)
        orBoard2[position] = "X"
        print(listtoboard((orBoard2)))
        if check_winner(orBoard2):
            win = "HUMAN"

        piece = random.choice(choice)
        orBoard2[piece] = "0"
        print(listtoboard(orBoard2))
        choice.remove(piece)
        if check_winner(orBoard2):
            win = "AI"
