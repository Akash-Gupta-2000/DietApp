import sqlite3

# Function will create the SQL Database table and populate it with the values from foodList.txt
def createTableandPopulate():
    
    conn = sqlite3.connect('foodList.db')
    c = conn.cursor()

    # Creates the table
    c.execute("""CREATE TABLE food (
              foodName text,
              foodServing text,
              fat integer,
              calories integer,
              carbs integer,
              protein integer,
              vegetarian text
              )""")
    conn.commit()

    file = open("foodList.txt", "r")    
    
    while True:
        try:
            line = file.readline()
            foodName, foodServing, fatGrams, calories, carbGrams, proteinGrams, vegetarian = line.split("@")

            # Cast the string values into integers for SQL input
            fatGrams = int(fatGrams)
            calories = int(calories)
            carbGrams = int(carbGrams)
            proteinGrams = int(proteinGrams)


            # Line will input the values into the SQL database
            c.execute("INSERT INTO food VALUES (:foodName, :foodServing, :fat, :calories, :carbs, :protein ,:veg)",
                      {'foodName': foodName, 'foodServing': foodServing, 'fat': fatGrams, 'calories': calories, 'carbs': carbGrams, 'protein': proteinGrams , 'veg': vegetarian})
            conn.commit()
            print(line)
        except ValueError:
            False
    conn.close()



