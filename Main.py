import mysql.connector as mys
mycon = mys.connect(host = 'localhost', user = 'root', passwd = 'LoremIpsum')
c = mycon.cursor()

c.execute("create database SK")
c.execute("use SK")
c.execute("create table Pantry (ItemNo integer primary key, Name varchar(30), Qty integer, Calorie integer, Expiry Date)")
c.execute("create table Recipes (RecipeNo integer primary key, Name varchar(30), Ingredients varchar(200), NetCalorie integer)")
mycon.commit()