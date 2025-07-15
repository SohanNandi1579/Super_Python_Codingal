def changecalculator(total: float, already_payed: float) -> float:
    """
    Calculates change to be given back
    :param total: Total bill
    :param already_payed: Money already payed
    :return: Amount of money to be returned as 'change'
    """
    return total - already_payed

print(changecalculator(4, 2.5))