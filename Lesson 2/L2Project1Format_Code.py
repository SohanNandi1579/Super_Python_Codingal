def system_checker(authorisation: str) -> str:
    """System checker checks the program and sees if the laptop is ready to shut down.
    :param authorisation: User Authorisation
    :type authorisation: str
    :return: Final Command
    :rtype: str
    """
    if "yes" in authorisation.casefold():
        return "Shutting Down in 3...\n\t2...\n\t1...\n\tGo!"
    elif "no" in authorisation.casefold():
        return "Mission Shutting Down Aborted"
    else:
        return "Sorry, cannot be processed"
    

userdefinition = input("Would you like to sign off and shut down your FireBolt?")
print("Shutdown Official V1579.299 (Newest Bugs deactivated, error fixed). ")
print(system_checker(userdefinition))