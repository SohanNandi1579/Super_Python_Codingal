def intersection_between_sets(myFavSet1: set, myFavSet2: set, flag=0) -> str:
    """
    Intersection of 2 sets
    :param myFavSet1: Set1
    :param myFavSet2: Set2
    :return: None
    """
    user_input = input("Enter values for your set (type '0' or 'q' to quit):")

    if user_input == '0' or user_input == 'q':
        confirmation = bool(input("Enter True(if you want to quit) or just enter click(if you don't want to quit): "))
        if confirmation == False:
            pass
        else:
            print(f"MyFavSet1: {myFavSet1}, MyFavSet2: {myFavSet2}, Intersection: {myFavSet1.intersection(myFavSet2)}")
            return ""

    elif flag == 0:
        myFavSet1.add(user_input)
        flag = 1

    elif flag == 1:
        myFavSet2.add(user_input)
        flag = 0

    intersection_between_sets(myFavSet1, myFavSet2, flag)


intersection_between_sets(set(), set())







