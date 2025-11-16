class circle:
    def __init__(self, radius):
        self.radius = radius
        self.__pi = 3.14
    def __area(self):
        return (self.__pi * self.radius ** 2)
    def perimeter(self):
        return (2 * self.__pi * self.radius)
    def __len__(self):
        return  int(self.perimeter())
c1=circle(5)
c1.pi = 5
print(len(c1))