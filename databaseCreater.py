# Program will create an SQL Database, parse the food list entries and enter them into the SQL Database
import sqlite3

"""
NOTES: How to insert a variable into an SQL Table:
format:
c.execute("INSERT INTO food VALUES (:foodName, :calories, :protein, :carbs, :protein, :fat)",
    {'foodName': FOODNAMEVARIABLE, 'calories': CALORIESVARIABLE, etc...})
"""


# Function will create the SQL Database table and populate it with the values from foodList.txt
def createTableandPopulate():
    # Creates the database and connection
    # c will be our cursor
    conn = sqlite3.connect('foodlist.db')
    c = conn.cursor()

    # Creates the table
    c.execute("""CREATE TABLE food (
              foodName text,
              foodServing text,
              fat integer,
              calories integer,
              carbs integer,
              protein integer
              )""")
    conn.commit()

    file = open("foodList.txt", "r")    # Opens the foodList.txt file in read mode
    # Will loop through and print every piece of information seperately
    #for line in file:
    while True:
        try:
            line = file.readline()
            foodName, foodServing, fatGrams, calories, carbGrams, proteinGrams = line.split("@")

            # Cast the string values into integers for SQL input
            fatGrams = int(fatGrams)
            calories = int(calories)
            carbGrams = int(carbGrams)
            proteinGrams = int(proteinGrams)


            # Line will input the values into the SQL database
            c.execute("INSERT INTO food VALUES (:foodName, :foodServing, :fat, :calories, :carbs, :protein)",
                      {'foodName': foodName, 'foodServing': foodServing, 'fat': fatGrams, 'calories': calories, 'carbs': carbGrams, 'protein': proteinGrams})
            conn.commit()
            print(line)
        except ValueError:
            False
    conn.close()



