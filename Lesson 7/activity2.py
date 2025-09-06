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
        for char in iterator:
            number += 1
        if number > 2:
            if iterator[0] == iterator[-1]:
                myEmptyDict[myList.index(iterator)] = [[iterator], [list.count(iterator)]] # Value1 = Word
                # name, Value2 = No. of times of occurences
        else:
            break

    return myEmptyDict



myWordsList = ["and", "hi", "bob"]
print(passer(myWordsList))