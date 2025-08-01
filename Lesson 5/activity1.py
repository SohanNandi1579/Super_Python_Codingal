import random


log = {}
while True:
    s=random.random()
    choice=random.choice(['rock', 'paper','scissors'])
    user = input("enter rock paper or scissors : ")
    if user.casefold() not in ['rock','paper','scissor'] :
        print("invalid input")
        continue

    log[s]=[choice,user]