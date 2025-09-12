def passer(myList: list) -> bool:
    """
    This is a function that says 'pass'
    only if the words given have same intial and final letters and
    the words have more than 2 letters.
    :param myList: Will contain list of words that we need to check
    :return: True or False
    """
    number = 0
    index = 0
    myEmptyDict = {}
    for iterator in myList:
        iterator = str(iterator)
        if iterator != None and [iterator, myList.count(iterator)] not in myEmptyDict.values():
            for char in iterator:
                number += 1
            if number > 2:
                if iterator[0] == iterator[-1]:
                    myEmptyDict[index] = [iterator, myList.count(iterator)] # Value1 = Word
                    # name, Value2 = No. of times of occurences
            else:
                break
            index+=1

    return myEmptyDict


myWordsList = ["and", "hi", "bob", "bob", None, 6, 6, 424, "hello, my name is noah", "finer", "racecar"]
print(passer(myWordsList))