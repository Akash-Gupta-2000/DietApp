import math
import sqlite3
import databaseCreater
import foodSearchClass
import dailyIntakeClass
from dailyIntakeClass import dailyIntake

print("Welcome to the diet app\n")

age = int(input("Enter your age in years:"))
weightKilos = int(input("Enter your weight in Kilos:"))
print('Enter Your Height:')
heightFeet = int(input("feet:"))
heightInch = int(input("inches:"))


while True:
    gender = bool(input("\nEnter your gender:\n0 for male\n1 for female:\n"))
    hours=float(input("Enter your hours of workout/exercise:"))
    #PA = int(input("\nEnter your physical Activity level\n0 for Sedentary\n1 for Low Active\n2 for Active\n3 for Very Active\n"))
    if 0<=hours<=1: 
        PA=0
    elif 1<hours<=2 : 
        PA=1
    elif 2<hours<=3 :
        PA=2
    elif hours>3 :
        PA=3
    else :
        print("Time cannot be negative!")
    if gender == 0: # Male
        if PA == 0:
            PA = 1.0
            break
        elif PA == 1:
            PA = 1.12
            break
        elif PA == 2:
            PA = 1.27
            break
        elif PA == 3:
            PA = 1.54
            break
        else:
            print("Incorrect Physical Activity Level Entered.")
    elif gender == 1: # Female
        if PA == 0:
            PA = 1.0
            break
        elif PA == 1:
            PA = 1.14
            break
        elif PA == 2:
            PA = 1.27
            break
        elif PA == 3:
            PA = 1.45
            break
        else:
            print("Incorrect Physical Activity Level Entered.")
    else:
        print("Incorrect Gender Value Entered.")


height = (heightFeet*.3048)+(heightInch*0.0254)    # Height is now in Meters

# TEE will hold the daily amount of calories the person burns (Total Energy Expenditure)
if gender == 0:
    TEE = 864-9.72*age+PA*(14.2*weightKilos+503*height)
    math.ceil(TEE)
elif gender == 1:
    TEE = 387-7.31*age+PA*(10.9*weightKilos+660.7*height)
    math.ceil(TEE)

veg = input("\nAre you Vegetarian?:\n1 for Veg \n0 for Non Veg:\n")
disease = input("\nEnter the Disease name you are suffering from, if any, otherwise enter 'None'\n")

# Lose Weight: carbs 40%, protein 35%, fat 25% of diet
# Maintain Weight: carbs 50%, protein 25%, fat 25% of diet
# Gain Muscle: carbs 45%, protein 35%, fat 20% of diet

dietaryChoice = int(input("\nWould you like to gain(0), maintain(1), or lose weight(2)?\n"))

# These three functions will determine the calories of each
# Macro Nutrient for a given TEE and returns a Tuple
def loseWeightMacros(TEE):
    carbsCal = TEE * .4
    fatCal = TEE * .25
    proteinCal = TEE * .35
    return (carbsCal, proteinCal, fatCal)

def maintainWeightMacros(TEE):
    carbsCal = TEE * .5
    fatCal = TEE * .25
    proteinCal = TEE * .25
    return (carbsCal, proteinCal, fatCal)

def gainWeightMacros(TEE):
    carbsCal = TEE * .45
    fatCal = TEE * .20
    proteinCal = TEE * .35
    return (carbsCal, proteinCal, fatCal)

if dietaryChoice == 1:
    carbsCal, proteinCal, fatCal = maintainWeightMacros(TEE)
elif dietaryChoice == 2:
    deficitAmount = 300     
    TEE -= deficitAmount
    carbsCal, proteinCal, fatCal = loseWeightMacros(TEE)
elif dietaryChoice == 0:
    surplusAmount = 300     
    TEE += surplusAmount
    carbsCal, proteinCal, fatCal = gainWeightMacros(TEE)


# Protein and Carbs = 4 cal per gram, Fat = 9 cal per gram
proteinGram = math.ceil(proteinCal / 4)
carbsGram = math.ceil(carbsCal / 4)
fatGram = math.ceil(fatCal / 9)

userIntake = dailyIntake(TEE, proteinGram, carbsGram, fatGram)

conn = sqlite3.connect('foodList.db')

c = conn.cursor()   

while True:
    meal1 = input("\nEnter what you have eaten today, type exit to stop:")
    if meal1 == "exit":
        break
    c.execute("SELECT * FROM food WHERE foodName like :name", {'name': '%'+meal1+'%'})

    try:
        foodSearchList = []

        table = c.fetchall()
        i = 0
        for row in table:  
            cName, cServing, cFat, cCal, cCarb, cProtein ,cVeg= table[i]     
            foodSearchList.append(foodSearchClass.foodItem(cName, cServing, cFat, cCal, cCarb, cProtein, cVeg))
            i += 1

        i = 0
        for entries in foodSearchList:
            print(i)
            foodSearchList[i].printer()
            i += 1

        choice = int(input("Type in the number of the result corresponding to your food:")) 
        foodCal, foodProtein, foodCarb, foodFat = foodSearchList[choice].getValues()
        userIntake.updateIntake(int(foodCal), int(foodProtein), int(foodCarb), int(foodFat))
        userIntake.printIntake()   


    except TypeError:
        print("Error, search not in table")

if userIntake.TEE > userIntake.calorieCount:
    print("You currently have ", int(userIntake.TEE)-userIntake.calorieCount," calories remaining for the day")
else:
    print("You have eaten ", userIntake.calorieCount-int(userIntake.TEE), " calories too many today")


if userIntake.proteinG > userIntake.proteinIntake:
    print("You currently have", userIntake.proteinG-userIntake.proteinIntake, " grams of protein remaining for the day")
else:
    print("You have eaten ", userIntake.proteinIntake-userIntake.proteinG, " grams too many of protein")


if userIntake.carbG > userIntake.carbIntake:
    print("You currently have", userIntake.carbG-userIntake.carbIntake, " grams of carbs remaining for the day")
else:
    print("You have eaten ", userIntake.carbIntake-userIntake.carbG, " grams too many of carbs")


if userIntake.fatG > userIntake.fatIntake:
    print("You currently have", userIntake.fatG-userIntake.fatIntake, " grams of carbs remaining for the day")
else:
    print("You have eaten ", userIntake.fatIntake-userIntake.fatG, " grams too many of fat")


print("\nAlternative Diet Suggestions are:")
remCalories=int(userIntake.TEE)-userIntake.calorieCount

c.execute("SELECT * FROM food WHERE calories BETWEEN ? and ?",(remCalories-50 , remCalories+50))
foodSearchList = []

table = c.fetchall()
i = 0
for row in table:  
    cName, cServing, cFat, cCal, cCarb, cProtein,cVeg = table[i]     
    foodSearchList.append(foodSearchClass.foodItem(cName, cServing, cFat, cCal, cCarb, cProtein,cVeg))
    i += 1

i = 0
for entries in foodSearchList:
    print(i+1)
    foodSearchList[i].printer()
    i += 1



