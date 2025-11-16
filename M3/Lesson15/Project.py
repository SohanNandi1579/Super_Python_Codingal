class vehicle:
    def __init__(self, seat, milage, avg_price):
        self.seat = seat
        self.milage = milage
        self.average_fare_price = avg_price
    def total_fare(self):
        return self.seat * self.average_fare_price

class bus(vehicle):
    def __init__(self, seat, milage, avg_price):
        super().__init__(seat, milage, avg_price)
        self.busfare = vehicle.total_fare(self) * 1.1
    def disp(self):
        print(self.busfare)

bus1 = bus(50, 20, 1000)
bus1.disp()
