class car:
    flag=0
    no_wheels = 4  #class variable
    has_engine=True
    def __init__(self,model,color,top_speed):
        self.model = model    #instance variable
        self.color = color
        self.top_speed = top_speed

    def milage(self,km_travelled,fuel_used):
        mlg=km_travelled/fuel_used
        print(f"the milage of {self.model} is {mlg} km")

#object or instance of a class
audi=car("audi","red",200)
bmw=car("bmw","black",250)

print(audi.model)

print(car.no_wheels)


# audi={model: "audi",
#       color:"red",
#       top_speed:200}

