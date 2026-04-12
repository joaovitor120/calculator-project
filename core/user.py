from datetime import datetime
import sqlite3
import os
from dotenv import load_dotenv 

load_dotenv() #This loads variables from .env into os.environ
adm_password = os.getenv("ADM_PASSWORD")
if not adm_password:
    raise EnvironmentError("ADM_PASSWORD not defined at environment variables.")
connection = sqlite3.connect("./database/database.db")
cursor = connection.cursor()

cursor.execute("""
SELECT Name FROM User 
""")
Names = cursor.fetchall()
NamesList = ["adm"]
for i in Names:
    NamesList.append(str(i)[2:-3])
now = datetime.now()
#function input --> get datas from user and verified if username is available
def avoid_SQL_injection(user_input):
    if "'" in user_input or '"' in user_input:
        return user_input.replace('"', '').replace("'", '')
    else:
        return user_input
def WelcomeUser():
    bdayYear = False
    repeated_user = input("Do you already use JVBCalculator(Y/N)? ").strip().upper()
    while repeated_user != 'Y' and repeated_user != "N":
        print("Please, type only Y or N")
        repeated_user = input("Do you already use JVBCalculator(Y/N)? ").strip().upper()
    
    if repeated_user == "N":
        name_input = (input("Which username do you wanna be called? ")) 
        name = avoid_SQL_injection(name_input) #to avoid SQL injection 
        if name_input != name:
            print("Names with '' or " + f'"" are not accepted, your username was changed to {name}')
        while name in NamesList:
            name_input = input("This username is not available, please select another username: ")
            name = avoid_SQL_injection(name_input)
            if name_input != name:
                print("Names with '' or " + f'"" are not accepted, your username was changed to {name}')
        age = int(input(f"How old are you, {name}? "))
        year = int(now.strftime("%Y"))
        bday = input("Do you already make birthiday this year?(Y/N)").upper()

        if bday == "Y":
            bdayYear = True
        yearBorn = year - age - (0 if bdayYear else 1) #remove 1 year from year born if already make birthday or 0 if not
        user = {
            "Name": name,
            "Year Born": yearBorn,
            "Age": age,
            "New": True
        }
    elif repeated_user == "Y":
        name = input("Type your username: ")
        while name not in NamesList:
            name = input("I could not find you username at my database, please type your username again: ")
        if name == "adm":
            #adm_password = '123'
            adm_password_input = input("Hello, adm, please type the master password: ").strip()
            while adm_password_input != adm_password:
                print("This is not the master password. ")
                adm_password_input = input("Please type the master password: ").strip()
            user = {
                "Name" : name
            }
        else:

            cursor.execute(f"""
            SELECT Year_born, Age FROM User WHERE Name = '{name}'
            """)
            dataset_user_data = cursor.fetchall()
            dataset_data = []
            for i in dataset_user_data[0]:
                dataset_data.append(i)

            yearBorn, age = dataset_data
            user = {
            "Name": name,
            "Year Born": yearBorn,
            "Age": age,
            "New": False
            }
        
    return user #return a dict with user infos

#function output
def show_user_data(user):
    for i in user:
        user_datas = f"{i}:{user[i]}" #to show userdatas more friendly in print
        print(user_datas)