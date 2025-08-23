import mysql.connector as mys
mycon = mys.connect(host = 'localhost', user = 'root', passwd = '1234')
c = mycon.cursor()

c.execute("drop database SmartKitchen") # remove in final version
c.execute("create database if not exists SmartKitchen")
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

# (1,"egg",2,'2021-2-12')

ch = 'y'
while ch.lower() == 'y':
    print("\n MENU --- \n What would you like to do? \n 1. View available food stuffs \n 2. View available dishes \n 3. Update pantry's contents \n 4. Close")
    ans = int(input("> "))

    if ans == 1:
        c.execute("Select Itemno, name, qty from pantry where qty > 0")
        data = c.fetchall()
        if c.rowcount == 0:
            print("Empty Pantry.")
        else:
            for row in data:
                print(row)
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
        c.execute("select name from pantry where qty > 0")
        data = c.fetchall()
        PresentIngredients = []

        for row in data:
            PresentIngredients.append(row[0])

        count = 0    

        for i in RecipeEntries:
            isPresent = True
            NeedIngredients = i[4].split("-")

            for j in NeedIngredients:
                if j not in PresentIngredients:
                    isPresent = False
                    break

            if isPresent:
                print("Recipe", i[1], "can be made.")
                count += 1
                ans = input("Would you like to create it? (y/n)")

                if ans.lower() == 'y':
                    for j in NeedIngredients:
                        c.execute(
                            "update pantry set qty = qty - 1 where name = %s",
                            (j,)
                        )
                        mycon.commit()
                    print("Enjoy your dish")
                else:
                    print("Alright...")

        # after the loop finishes
        if count == 0:
            print("No recipes can be made")


    elif ans == 3:
        name = input("Enter ingredient's name: ")
        qty = int(input("Enter quantity: "))
        exp = input("Enter expiry date: ")

        c.execute("insert into pantry (Name, Qty, Expiry) values ('{0}', {1}, '{2}')".format(name, qty, exp))

    elif ans == 4:
        print("Farewell.")
        ch = 'n'
    
    else:
        print("Invalid option.")
    
