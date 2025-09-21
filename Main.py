# Made by Siddarth, Ruben, and Sivadath from 12C

from datetime import date

import mysql.connector as mys
mycon = mys.connect(host = 'localhost', user = 'root', passwd = '1234')
c = mycon.cursor()

def print_table(L):
    def print_border():
        print("+", end = "")
        for i in lens:
            print("-"*(i+2)+"+", end = "")
        print()

    L = list(L)

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
    print_border()

c.execute("drop database if exists SmartKitchen") # Remove in Final Version
c.execute("create database SmartKitchen")
c.execute("use SmartKitchen")
c.execute("create table Pantry (ItemNo integer primary key auto_increment, Name varchar(30), Qty integer, Expiry date)")
c.execute("create table Recipes (RecipeNo integer primary key, Name varchar(30), Qty integer, Calorie integer, Ingredients varchar(255))")
c.execute("create table AvailableRecipes (RecipeNo integer, ItemNo integer, Qty Integer, primary key (ItemNo, RecipeNo), foreign key (ItemNo) references Pantry(ItemNo), foreign key (RecipeNo) references Recipes(RecipeNo))")

RecipeEntries = [
    (1, "Omlete", 1, 154, "egg-salt-pepper-oil"),
    (2, "Bread", 1, 265, "flour-yeast-oil-salt-water"),
    (3, "Rice", 1, 130, "rice-water-salt"),
    (4, "Oat Meal", 1, 70, "oats-water-milk-salt"),
    (5, "Dosa", 1, 130, "rice-urad dal-water-salt-oil"),
    (6, "Masala Dosa", 1, 225, "rice-urad dal-water-salt-oil-potato-onion-chili-spices"),
    (7, "Idli", 1, 61, "rice-urad dal-water-salt"),
    (8, "Sambhar", 1, 260, "toor dal-tamarind-vegetables-onion-tomato-sambhar powder-chili-mustard seeds-curry leaves-oil"),
    (9, "Coconut Chutney", 1, 60, "coconut-green chili-ginger-curry leaves-salt-water"),
    (10, "Boiled Egg", 1, 78, "egg-water-salt")
]

for i in RecipeEntries:
    c.execute("insert into Recipes values" + str(i))
mycon.commit()

go = True
while go:
    current_date = str(date.today())

    print("\n MENU \n What would you like to do? \n 1. View available food stuffs \n 2. View available dishes \n 3. Update pantry's contents \n 4. Close \n")
    ans = int(input("> "))
    print()

    c.execute("select itemno from pantry where qty <= 0 or expiry < '{0}'".format(current_date))
    data = c.fetchall()
    for row in data:
        c.execute("delete from pantry where itemno = '{0}'".format(row[0]))
    mycon.commit()

    if ans == 1:
        c.execute("select itemno, name, qty from pantry")
        data = c.fetchall()

        if c.rowcount == 0:
            print("Your pantry is empty.")

        else:
            print_table(data)
            eat1 = input("Would you like to take an item? (y/n): ")

            if eat1.lower() == 'y':
                eat2 = int(input("Enter the code of the item you would like to take: "))
                c.execute("select name from pantry where ItemNo = {0}".format(eat2))
                item = c.fetchone()
                print(item)
                c.execute("Delete from pantry where ItemNo = {0}".format(eat2))
                mycon.commit()
                print("Item", item[0], "removed from pantry")

            else:
                print("Alright.")
       
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
            print("\nRecipes you can make:")
            for r in AvailableRecipes:
                print(r[0], "-", r[1])

            choice = int(input("Enter the recipe number you want to create: "))

            selected = None
            for r in AvailableRecipes:
                if r[0] == choice:
                    selected = r
                    break

            if selected is not None:
                NeedIngredients = selected[4].split("-")
                for j in NeedIngredients:
                    c.execute("update pantry set qty = qty - 1 where name = '{0}'".format(j))
                    mycon.commit()
                print("Enjoy your", selected[1], "!")

            else:
                print("Invalid choice.")

    elif ans == 3:
        name = input("Enter ingredient's name: ")
        qty = int(input("Enter quantity: "))
        exp = input("Enter expiry date (YYYY-MM-DD): ")

        c.execute("insert into pantry (Name, Qty, Expiry) values ('{0}', {1}, '{2}')".format(name, qty, exp))

    elif ans == 4:
        print("Farewell.")
        go = False
    
    else:
        print("Invalid option.")
