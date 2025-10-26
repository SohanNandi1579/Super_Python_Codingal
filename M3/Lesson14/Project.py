import math


class Circle:
    def __init__(self):
        self.radius = float(input("Enter your radius: "))

    def perimeter(self):
        return 2*math.pi*self.radius

    def area(self):
        return math.pi*self.radius**2


run = Circle()
print(f"Perimeter: {run.perimeter(): .2f}")
print(f"Area: {run.area(): .15f}")