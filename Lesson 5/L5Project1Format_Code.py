import math


Functions = {1: "sin",
             2: "cos",
             3: "tan",
             4: "cosec",
             5: "sec",
             6: "cot",
             }

for key, value in Functions.items():
    print(f"{key}: {value}")
in_deg = int(input("Enter your value in degrees please: "))
chooseyr = int(input("Enter your function: "))

in_rad = math.radians(in_deg)
if in_rad == (in_deg*math.pi/180):
    print("All is well")


if Functions[chooseyr] == "sin":
    result = math.sin(in_rad)
elif Functions[chooseyr] == "cos":
    result = math.cos(in_rad)
elif Functions[chooseyr] == "tan":
    result = math.tan(in_rad)
elif Functions[chooseyr] == "cosec":
    result = 1 / math.sin(in_rad)
elif Functions[chooseyr] == "sec":
    result = 1 / math.cos(in_rad)
elif Functions[chooseyr] == "cot":
    result = 1 / math.tan(in_rad)
else:
    result = "Invalid"

print(f"The {Functions[chooseyr]} of {in_deg}° a.k.a. {in_rad} rad is {result}.")
