import mysql.connector as mys
mycon = mys.connect(host = 'localhost', user = 'root', passwd = '1234')
c = mycon.cursor()

c.execute("drop database SK") # Remove this in the final version
c.execute("create database if not exists SK")
c.execute("use SK")
c.execute("create table Pantry (ItemNo integer primary key auto_increment, Name varchar(30), Qty integer, Expiry date)")
c.execute("create table Recipes (RecipeNo integer primary key, Name varchar(30), Qty integer, Calorie integer)")
c.execute("create table RecipeIngredients (RecipeNo integer, ItemNo integer, Qty Integer, primary key (ItemNo, RecipeNo), foreign key (ItemNo) references Pantry(ItemNo), foreign key (RecipeNo) references Recipes(RecipeNo))")

RecipeEntries = [(1,"Omlete",1,154),
                 (2,"Bread",1,265),
                 (3,"Rice",1,130),
                 (4,"Oat Meal",1,70),
                 (5,"Dosa",1,130),
                 (6,"Masala Dosa",1,225),
                 (7,"Idli",1,61),
                 (8,"Sambhar",1,260),
                 (9,"Coconut Chutney",1,60),
                 (10,"Boiled Egg",1,78)]

for i in RecipeEntries:
    c.execute("insert into Recipes values" + str(i))

mycon.commit()

# (1,"egg",2,'2021-2-12')

ch = 'y'
while ch.lower() == 'y':
    print("--- MENU --- \n What would you like to do? \n 1. View available food stuffs \n 2. View available dishes \n 3. Update pantry's contents")
    ans = int(input("> "))
    if ans == 1:
        c.execute("Select * from pantry")
        data = c.fetchall()
        for row in data:
            print(row)
        eat1 = input("Would you like to take an item? (y/n): ")
        if eat1.lower() == 'y':
            eat2 = int(input("Enter the code of the item you would like to take: "))
            c.execute("select name from pantry where ItemNo = {}".format(eat2))
            item = c.fetchone()
            c.execute("Delete from pantry where ItemNo = {}".format(eat2))
            mycon.commit()
            print("Item", item[1], "removed from pantry")
        else:
            print("Alright.")

    elif ans == 2:


    elif ans == 3:
        name = input("Enter ingredient's name: ")
        qty = int(input("Enter quantity: "))
        exp = input("Enter expiry date: ")
        c.execute("insert into pantry (Name, Qty, Expiry) values ({}, {}, {})").format(name, qty, exp)
