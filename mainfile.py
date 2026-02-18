import time
import os
import json
from datetime import datetime

now = datetime.now()
now = datetime.now()
hour_formated = now.strftime("%H:%M") #get hour data
day_formated = now.strftime("%d/%m/%Y") #get day data

operations_available = {
    "+": lambda a,b: (f"{a} + {b} = {a+b}"),
    "-": lambda a,b: (f"{a} - {b} = {a-b}"),
    "*": lambda a,b: (f"{a} * {b} = {a*b}"),
    "/": lambda a,b: (f"{a} / {b} = {a/b}") 
} #lambda for each operation type

#function input --> get datas from user
def WelcomeUser():
    bdayYear = False
    year = int(input("Which year we are? "))
    bday = input("Do you already make birthiday this year?(Y/N)").upper()

    if bday == "Y":
        bdayYear = True
    name = input("What is your name? ")
    age = int(input("How old are you? "))
    yearBorn = year - age - (0 if bdayYear else 1) #remove 1 year from year born if already make birthday or 0 if not
    user = {
        "Name": name,
        "Year Born": yearBorn,
        "Age": age
    }
    return user #return a dict with all user info

#function output
def show_user_data(user):
    for i in user:
        user_datas = f"{i}:{user[i]}" #to show userdatas more friendly in print
        print(user_datas)
#function output
def operation(op,n1,n2):
    return operations_available[op](n1,n2) #use the dict with lambdas to execute each operations

def validate_number(msg): #number validate, to see if the number is an integer
    while True: 
        try:
            return int(input(msg)) #for now only accept int values from input
        except ValueError: #if number insert not an integer type
            print("Invalid number. Try again.")
def get_valid_operation(operation): #operation verification, i only want operations inputs availables
        while operation not in operations_available: #if the operations type not is includede in operations available dict
            print("Invalid operation, select only one of them:(+,-,/,*)")
            operation = input("Which operation do you wanna make((+)/(-)/(*)/(/))? ").strip() #strip to remove blank spaces
        return operation # when it get out loop
            
            
def get_operation(): #get input operation
    return input("Which operation do you wanna make((+)/(-)/(*)/(/))? ").strip() #strip to remove blank spaces

def get_numbers(): #input function
    num1 = validate_number(("Type the first number: "))
    num2 = validate_number(("Type the second number: "))
    return num1, num2
def calculate(op,n1,n2):#executable function
    result = operation(op, n1, n2)
    return result

def exit_program(user,op,n1,n2): #this function was created to set a flag when the users want to get out
    return "EXIT"

menu = { #dict with functions inserted
    "1": calculate,
    "2": show_user_data,
    "3": exit_program
}

def menufunc():
    print("\n MENU: \n 1:Calculator \n 2:My Informations \n 3:Exit")
    optionmenu = input("Choose one of them options(1/2/3): ")
    while optionmenu not in menu:
        print("Invalid option. Please choose 1, 2, or 3.")
        optionmenu = input("Choose one of them options(1/2/3): ")
    return optionmenu

def add_user(userdata, file="userinfos.json"):
    array1 = []
    with open(file, "r") as f:
        content = f.read().strip()
    if content:
        content_decoded = json.loads(content) #json  str format into python object
        for i in content_decoded:
            array1.append(i)
        array1.append(userdata)
        json_data = json.dumps(array1, indent=4)
        with open("userinfos.json", "w") as f:
            f.write(json_data)

def main():
    user = WelcomeUser()
    user_datas_dict = user.copy()
    user_datas_dict.update({
        "Hours": hour_formated,
        "Day": day_formated
    })
    add_user(user_datas_dict)



    print(f"Welcome, Mr {user['Name']}, born in {user['Year Born']}, you receive an access to the JVBCalculator")
    
    """
    jsonusers = json.dumps(user)
    with open("userinfos.json", "a") as userinfojson:
        if userinfojson.tell() > 0:
            userinfojson.write(f"")
        userinfojson.write(f"\n{jsonusers}")
    """
    while True:
        optionmenu = menufunc()
        if optionmenu == "1":
            try:
                calctype = get_operation()
                operation = get_valid_operation(calctype)
                num1, num2 = get_numbers()
                result = menu[optionmenu](operation,num1,num2)
                print(f"Result {result}")
            except ZeroDivisionError:
                print("Division by zero is not allowed")
        elif optionmenu == "2":
            result = menu[optionmenu](user)
        elif optionmenu == "3":
            print("Goodbye! See you later!")
            break
        time.sleep(1)

main()