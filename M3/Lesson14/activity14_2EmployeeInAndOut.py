import random
import time

class SchoolOfCriminals:
    def __init__(self, empName, empAge, empBranch, empSalary):
        self.name = empName
        self.age = empAge
        self.Branch = empBranch
        self.Salary = empSalary
        self.WantToGetKickedOut = bool(input("Please enter True or False: - 'Do You Want To Get Kicked Out?:  "))

    def confidential(self):
        self.phoneNumber = input("Please enter your Phone Number: ")
        self.address = input("Please enter your address: ")
        self.LifeChoicesHistory = input("Please enter your life choices history: ")

    # def __del__(self):
    #     print("Let's fire some employees!!!!!")
    #     print("The lucky one to get kicked out is: *DrumRoll* ")
    #     for i in range(5, -1, -1):
    #         print(f"{i}...")
    #         print("\n"* 50)
    #     print(random.choice[])

class CriminalsManagement:
    def __init

emp1 = SchoolOfCriminals("Criminal", "12", "Department of Masterminded Criminal Activities", "100000000000 USD")
emp1.confidential()
del emp1
print("Criminal_1321, you're deleted for helping an old woman cross the street instead of murdering her.")