class CriminalPoint:
    def __init__(self, criminalix, criminaly):
        self.x = criminalix
        self.y = criminaly

    def __str__(self):
        return f"{self.x},{self.y}"

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return f"{x},{y}"

point_blankrangeshooter = CriminalPoint(1, 2)
Colt33_extrablood = CriminalPoint(3, 5)
print(point_blankrangeshooter + Colt33_extrablood)
print(str(point_blankrangeshooter))