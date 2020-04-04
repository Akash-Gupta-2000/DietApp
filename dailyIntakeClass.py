# Class will hold the TEE value for the day, as well as track how
# Many calories the user has consumed for the day
# And calculate the grams of each macro nutrient consumed

class dailyIntake():
    def __init__(self, TEE, proteinG, carbG, fatG):
        self.TEE = TEE
        self.proteinG = proteinG
        self.carbG = carbG
        self.fatG = fatG
        self.calorieCount = 0
        self.proteinIntake = 0
        self.carbIntake = 0
        self.fatIntake = 0

    def updateIntake(self, calories, protein, carbs, fat):
        self.calorieCount += calories
        self.proteinIntake += protein
        self.carbIntake += carbs
        self.fatIntake += fat

    def printIntake(self):
        print("Total Amount of Calories consumed Today:", self.calorieCount, " calories/", int(self.TEE), " calories total", sep="")
        print("Total amount of protein eaten:", self.proteinIntake, "g/", self.proteinG, "g", sep="")
        print("Total amount of carbs eaten:", self.carbIntake, "g/", self.carbG, "g", sep="")
        print("Total amount of fat eaten:", self.fatIntake, "g/", self.fatG, "g", sep="")
