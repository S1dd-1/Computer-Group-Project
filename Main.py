# Made by Siddarth, Ruben, and Sivadath from 12C

from datetime import date, datetime, timedelta
import mysql.connector as mys
import csv

# Print graph via data given
def print_graph(Values):
    
    vals = [[d, round(int(c)/50)*50] for d, c in Values]
    qy = [y for x, y in vals]

    L = []
    L.append("     | 6 5 4 3 2 1 0")
    L.append("   0 +---------------")

    yy = list(range(50, max(qy) + 100, 50))
    for y in yy:
        str1 = ' ' * abs(len(str(y)) - 4) + str(y) + ' | '
        for _, yval in vals:
            if yval == y:
                str1 += 'x '
            else:
                str1 += '  '
        L.append(str1)

    L.reverse()
    for line in L:
        print(line)

# Track calorie intake and call print graph
def calorie_intake(today_calorie):

    print("You have consumed " + str(today_calorie) + " calories today")

    with open("CalorieIntake.csv",'r',newline='') as csvfile:
        Values = list(csv.reader(csvfile))

    last_date = date.fromisoformat(Values[-1][0])
    today_date = date.today()
    difference = (today_date - last_date).days

    if difference == 0:
        Values[-1][1] = str(today_calorie)

    elif 1 <= difference <= 7:
        del Values[:difference]
        for i in range(difference - 1, 0, -1):
            day = today_date - timedelta(days=i)
            Values.append([day.isoformat(), 0])
        Values.append([today_date.isoformat(), today_calorie])

    else:
        Values.clear()
        for i in range(6, 0, -1):
            day = today_date - timedelta(days=i)
            Values.append([day.isoformat(), 0])
        Values.append([today_date.isoformat(), today_calorie])

    with open("CalorieIntake.csv",'w',newline='') as csvfile:
        csv.writer(csvfile).writerows(Values)

    print_graph(Values)

# initialize calorie.csv if it does not exist
def calorie_initialize():
    today = date.today()
    Values = []

    for i in range(6, 0, -1):
        day = today - timedelta(days=i)
        Values.append([day.isoformat(), 0])

    Values.append([today.isoformat(), 0])

    with open("CalorieIntake.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(Values)

# Print mysql-esque table
def print_table(ColumnNames, L):
    def print_border():
        print("+", end = "")
        for i in lens:
            print("-"*(i+2)+"+", end = "")
        print()

    L = [ColumnNames] + L

    lens = []
    for i in L[0]:
        lens.append([])

    for i in range(len(L)):
        L[i] = list(L[i])
        for j in range(len(L[i])):
            L[i][j] = str(L[i][j])
            lens[j].append(len(L[i][j]))

    for i in range(len(lens)):
        lens[i] = max(lens[i])

    for i in range(len(L)):
        for j in range(len(L[i])):
            while len(L[i][j]) < lens[j]:
                L[i][j] += " "

    print_border()
    for i in range(len(L)):
        print("|", end = "")
        for j in range(len(L[i])):
            print(" "+L[i][j]+" ", end = "|")
        print()
        if i == 0:
            print_border()
    print_border()

# Connect to mysql
mycon = mys.connect(host = 'localhost', user = 'root', passwd = '1234')
c = mycon.cursor()

# Initialize database
# c.execute("drop database if exists SmartKitchen") # Remove in Final Version # Removed
c.execute("create database if not exists SmartKitchen")
c.execute("use SmartKitchen")
c.execute("create table if not exists Pantry (ItemNo integer primary key auto_increment, Name varchar(30), Qty integer, Expiry date)")
c.execute("create table if not exists Recipes (RecipeNo integer primary key, Name varchar(30), Qty integer, Calories integer, Ingredients varchar(255))")

c.execute("SELECT COUNT(*) FROM Recipes")
count = c.fetchone()[0]
if count == 0:
    RecipeEntries = [
        (1, "Omlete", 1, 154, "egg-salt-pepper-oil"),
        (2, "Bread", 1, 265, "flour-yeast-oil-salt-water"),
        (3, "Rice", 1, 130, "rice-water-salt"),
        (4, "Oat Meal", 1, 70, "oats-water-milk-salt"),
        (5, "Dosa", 1, 130, "rice-urad dal-water-salt-oil"),
        (6, "Masala Dosa", 1, 225, "rice-urad dal-water-salt-oil-potato"),
        (7, "Idli", 1, 61, "rice-urad dal-water-salt"),
        (8, "Sambhar", 1, 260, "toor dal-tamarind-vegetables-onion-salt"),
        (9, "Coconut Chutney", 1, 60, "coconut-green chili-ginger-salt-water"),
        (10, "Boiled Egg", 1, 78, "egg-water-salt"),
        (11, "Roti", 1, 120, "wheat flour-water-salt-oil"),
        (12, "Upma", 1, 180, "rava-water-onion-chili-oil-salt"),
        (13, "Poha", 1, 150, "poha-onion-chili-potato-oil-salt"),
        (14, "Curd Rice", 1, 180, "rice-curd-salt-oil-curry leaves"),
        (15, "Lemon Rice", 1, 190, "rice-lemon juice-turmeric-chili-oil-salt"),
        (16, "Vegetable Pulao", 1, 250, "rice-carrot-peas-onion-oil-salt"),
        (17, "Chapati Roll", 1, 210, "chapati-potato-onion-chili-salt"),
        (18, "Tomato Soup", 1, 90, "tomato-water-salt-pepper-butter"),
        (19, "Fruit Salad", 1, 95, "banana-apple-papaya-honey"),
        (20, "Corn Salad", 1, 120, "corn-onion-chili-lemon-salt"),
        (21, "Fried Rice", 1, 230, "rice-carrot-peas-onion-soy sauce-oil"),
        (22, "Aloo Curry", 1, 200, "potato-onion-tomato-chili-oil")
    ]

    for i in RecipeEntries: 
        c.execute("insert into Recipes values" + str(i))

mycon.commit()

try:
    f = open("CalorieIntake.csv",'r')
    f.close()
except FileNotFoundError:
    calorie_initialize()

# Track today's calorie intake
with open("CalorieIntake.csv",'r',newline='') as csvfile:
    Values = list(csv.reader(csvfile))
    last_logged_date = date.fromisoformat(Values[-1][0])
    if last_logged_date == date.today():
        today_calorie = int(Values[-1][1])
    else:
        today_calorie = 0

# Main
while True:
    current_date = date.today()
    current_time = datetime.now()

    # Menu
    print('\n## MENU ##')
    print_table(['#','What would you like to do?'],
                [[1,'View pantry items'],
                 [2,'View available dishes'],
                 [3,'View all dishes'],
                 [4,'Update pantry'],
                 [5,'Show past week\'s calorie intake'],
                 [" ", " "],
                 [8,'Delete pantry data'],
                 [9,'Delete calorie data'],
                 [" ", " "],
                 [0,'Exit']])
    try:
        ans = int(input("> "))
        print()
    except ValueError:
        print("\nInvalid option.")
        continue
    
    # Delete expired and non-existent ingredients
    c.execute("select itemno from pantry where qty <= 0 or expiry < '%s'"%(current_date,))
    data = c.fetchall()
    for row in data:
        c.execute("delete from pantry where itemno = '%s'"%(row[0],))
    mycon.commit()

    # Show ingredients
    if ans == 1:
        c.execute("select itemno, name, qty from pantry")
        data = c.fetchall()

        if not data:
            print("Your pantry is empty.")

        else:
            print_table(['Item No','Item Name','Quantity'],data)
            eat1 = input("Would you like to take an item? (y/n): ")

            if eat1.lower() == 'y':
                eat2 = int(input("Enter the code of the item you would like to take: "))
                c.execute("select name from pantry where ItemNo = %s"%(eat2,))
                item = c.fetchone()
                c.execute("update pantry set qty = qty-1 where ItemNo = %s"%(eat2,))
                mycon.commit()
                print("Item " + item[0] + " removed from pantry")

            else:
                print("Alright.")

    # Show available recipes
    elif ans == 2:
        c.execute("select name from pantry")
        data = c.fetchall()
        PresentIngredients = []
        for row in data:
            PresentIngredients.append(row[0])

        AvailableRecipes = []

        for i in RecipeEntries:
            isPresent = True
            NeedIngredients = i[4].split("-")

            for j in NeedIngredients:
                if j not in PresentIngredients:
                    isPresent = False
                    break

            if isPresent == True:
                AvailableRecipes.append(i)

        if len(AvailableRecipes) == 0:
            print("No recipes can be made")

        else:
            print("Recipes you can make:")

            #for r in AvailableRecipes:
                #print(str(r[0]) + " - " + r[1])
            print_table(['#','Recipe Name'], [[r[0], r[1]] for r in AvailableRecipes])
            choice = int(input("\nEnter the recipe number you want to create: "))

            selected = None
            for r in AvailableRecipes:
                if r[0] == choice:
                    selected = r
                    break

            if selected is not None:
                NeedIngredients = selected[4].split("-")

                for j in NeedIngredients:
                    c.execute("update pantry set qty = qty - 1 where name = '%s'"%(j,))
                    mycon.commit()
                
                c.execute("select Calories from Recipes where RecipeNo = %s"%(selected[0],))
                data = c.fetchone()
                today_calorie += data[0]

                print("Enjoy your " + selected[1] + "!")

            else:
                print("Invalid choice.")

    # Show all recipes
    elif ans == 3:
        c.execute("select * from Recipes")
        data = c.fetchall()
        print_table(['Recipe No','Recipe Name','Quantity','Calories','Ingredients'], data)

    # Enter new foodstuff
    elif ans == 4:
        name = input("Enter ingredient's name: ")
        qty = int(input("Enter quantity: "))
        exp = input("Enter expiry date (YYYY-MM-DD): ")

        c.execute("insert into pantry (Name, Qty, Expiry) values ('%s', %s, '%s')"%(name, qty, exp))
        mycon.commit()

    # Show calorie intake of past week and show graph
    elif ans == 5:
        print("Your calorie intake for today is, " + str(today_calorie) + "\n")
        calorie_intake(today_calorie)

    # Delete all foodstuff data
    elif ans == 8:
        c.execute("truncate table pantry")
        mycon.commit()
        print("Your pantry has been cleared!")

    # Reset calorie data
    elif ans == 9:
        today_date = date.today()

        with open("CalorieIntake.csv",'r',newline='') as csvfile:
            Values = list(csv.reader(csvfile))

        Values.clear()
        for i in range(6, 0, -1):
            day = today_date - timedelta(days=i)
            Values.append([day.isoformat(), 0])
        Values.append([today_date.isoformat(), 0])

        with open("CalorieIntake.csv",'w',newline='') as csvfile:
            csv.writer(csvfile).writerows(Values)
        
        today_calorie = 0
        print("Calorie reset!")

    # Exit
    elif ans == 0:
        print("Farewell.\n")
        break
    
    # Invalid option
    else:
        print("Invalid option.")
