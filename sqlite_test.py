import sqlite3

name = "wagner"
yb = 2008
age = 10
hours = "12"
day = "1"
db = "./database/testDatabase.db"
connection = sqlite3.connect(db)
cursor = connection.cursor()
columns = ["Name", "Year_born", "Age", "Hours", "Day"]
tables_formatted = (", ".join(i for i in columns))
cursor.execute("""
    CREATE TABLE IF NOT EXISTS User 
    (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        Year_born INTEGER NOT NULL,
        Age INTEGER NOT NULL,
        Hours TEXT NOT NULL,
        Day TEXT NOT NULL
        )
""")
cursor.execute("""
    SELECT Name FROM User
""")
Names = cursor.fetchall()
print(Names)
seen = []
duplicates = []
for i in Names:
    if i in seen:
        duplicates.append(i)
    else:
        seen.append(i)
print(duplicates)

for i in duplicates:
    print(str(i)[2:-3])


names_list = []
#for i in Names:
#    print(i)
#    names_list.append(str(i)[2:-3])
#    cursor.execute(f"""
#DELETE FROM User WHERE Name = '{str(i)[2:-3]}';
#""")
name_input = input("Type your name: ")
if name_input == name:
    cursor.execute(f"""
SELECT * FROM User WHERE Name = '{name_input}'
""")
user_data = cursor.fetchall()

if name not in names_list:
    cursor.execute(f"""
        INSERT INTO User
        ({tables_formatted}) VALUES
        ('{name}', {yb}, {age}, '{hours}', '{day}')""")
else:
    print("Ja ta")

connection.commit() #used everytime when i modify datas and need to permanentely save datas, like when i'm using INSERT, UPDATE OR DELETE
#connection.fetchall() --> used when i need to get datas from the dataset
