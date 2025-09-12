tup1 = (4, 3, 2, 2, -1, 18)
tup2 = (2, 4, 8, 8, 3, 2, 9)
counter1 = 1
counter2 = 1
for t in list(tup1):
    counter1 = counter1 * t

for t in list(tup2):
    counter2 = counter2* t

print(counter1, counter2, sep="; ", end="!")