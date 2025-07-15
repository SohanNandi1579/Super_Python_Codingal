def totalpayment(bill: float, tip: float) -> float:
    """This function will tell us how much we have to pay IRL. 
    (Tip% + Bill in Total Real Countable Money)
    :param bill: the total bill
    :type bill: float
    :param tip: the tip in percentage
    :type tip: float
    :return: total money needed to pay
    :rtype: float
    """

    return bill + (tip/100)*bill

try:
    money = float(input("Enter your bill: "))
    extra = float(input("Enter how much tip in percentage you will give(but without the '%' sign): "))
    print(totalpayment(money, extra))
except:
    print("Invalid Input, Rerun Program")