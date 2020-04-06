# Will create a small class that will hold the components of a food search in the sql database
# So the user can select which food they ate


class foodItem():
    def __init__(self, cName, cServing, cFat, cCal, cCarb, cProtein, cVeg):
        self.foodName = cName
        self.foodServing = cServing
        self.foodFat = cFat
        self.foodCal = cCal
        self.foodCarb = cCarb
        self.foodProtein = cProtein
        self.veg = cVeg

    def printer(self):
        print("Food Name:"+self.foodName+"Serving Size:"+self.foodServing+"Calories:"+str(self.foodCal)+"\n")

    def getValues(self):
        return(self.foodCal, self.foodProtein, self.foodCarb, self.foodFat)