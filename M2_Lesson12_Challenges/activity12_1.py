import random


myBoard = ["""top left |    top middle  | top right
        --------------------------------------------------
           middle left | middle middle  | middle right
        ---------------------------------------------------
           bottom left | bottom middle  | bottom right"""]

print(myBoard)

s = random.random()
chooser = random.choice(["aics", "user"])

originalBoard = ["topleft", "topmiddle", "topright", "middleleft", "middlemiddle", "middleright", "bottomleft", "bottommiddle", "bottomright"]
orBoard2 = originalBoard.copy()
def listtoboard(myList: list) -> list:
    """
    Gives list out.
    :param myList: the list to be edited on.
    :return: The new list in the new style
    """
    return (f"""{myList[0]}  |  {myList[1]}  |  {myList[2]}
------------------------------------------------------------------
                {myList[3]}  |  {myList[4]}  |  {myList[5]}
------------------------------------------------------------------
                {myList[6]}  |  {myList[7]}  |  {myList[8]}""")




while True:
    print("Let's play: ")
    if chooser == "aics":
        piece = random.randint(0, 9)
        orBoard2[piece] = "O"
        print(listtoboard(orBoard2))

        enter_user =




    else:
        pass