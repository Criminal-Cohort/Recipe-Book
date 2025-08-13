import mysql.connector as sql

db = sql.connect(host="localhost", user="root", passwd="")
cursor = db.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS RECIPES")
db.close()

mydb = sql.connect(host="localhost", user="root", passwd="", database="recipes")
mycursor = mydb.cursor()
mycursor.execute(
    "create table if not exists recipes (itemno int primary key, rname varchar(20), ing text, prtime int, instr text)")


def insert():
    itemno = int(input('Enter item number- '))
    rname = input('Enter recipe name - ')
    ing = input('Enter ingredients - ')
    prtime = int(input('Enter time taken to make (minutes)- '))
    instr = input('Enter the instructions- ')

    query = "insert into recipes values (%s, %s, %s, %s, %s)"
    mycursor.execute(query, (itemno, rname, ing, prtime, instr))
    mydb.commit()
    print('Record Added')


def view():
    mycursor.execute('select * from recipes')
    res = mycursor.fetchall()
    print('Recipes:- ')
    for i in res:
        print(i)


def search():
    name = input("Enter recipe name to search: ")
    query = "select * from recipes where rname=" + name
    mycursor.execute(query)
    res = mycursor.fetchone()
    count = mycursor.rowcount

    if count == 0 or res is None:
        print("Record not found :( ")
    else:
        print("Record Found")
        print("Recipe Name: ", res[1])
        print("Ingredients: ", res[2])
        print("Preparation Time: ", res[3])
        print("Instructions: ", res[4])


def delete():
    name = input("Enter recipe name to delete: ")
    query = "delete from recipes where rname=" + name
    mycursor.execute(query)
    mydb.commit()


def edit():
    name = input("Enter recipe name: ")
    query = "select * from recipes where rname=" + name
    mycursor.execute(query)
    res = mycursor.fetchone()
    count = mycursor.rowcount

    if count == 0 or res is None:
        print("Record not found :( ")
    else:
        print(res)
        choice = input("What do you want to edit? (ingredients/prep time/instructions):")

        if choice == "ingredients":
            new = input("Enter updated ingredients:")
            q = "update recipes set ing=%s where rname=%s"
        elif choice == "prep time":
            new = input("Enter updated prep time:")
            q = "update recipes set prtime=%s where rname=%s"
        elif choice == "instructions":
            new = input("Enter updated instructions:")
            q = "update recipes set instr=%s where rname=%s"
        else:
            print("Invalid Choice, try again")
            return

        mycursor.execute(q, (new, name))
        mydb.commit()
        print('Recipe Updated')


print("Welcome to your Digital Cookbook!")
print("~~~~~~~~~~~~~~~~~~~~~~~~~\n")

while True:
    print("--------------MAIN MENU—-----------")
    print("1. Add a New Recipe")
    print("2. Search for a Recipe")
    print("3. Delete a Recipe")
    print("4. Edit Recipe")
    print("5. Show All Recipes")
    print("6. Exit ")
    print("-------------------------------—-----------\n")

    ch = int(input("Choose operation (1-6): "))

    if ch == 1:
        insert()
    elif ch == 2:
        search()
    elif ch == 3:
        delete()
    elif ch == 4:
        edit()
    elif ch == 5:
        view()
    elif ch == 6:
        break
    else:
        print("Invalid Choice")

mycursor.close()
mydb.close()
