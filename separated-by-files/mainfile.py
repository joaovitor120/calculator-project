import time
import os
from datetime import datetime
import userFunctions
import calculate_file
import menuFunctions   
from json_files import json_insert_data
import math

now = datetime.now()
now = datetime.now()
hour_formated = now.strftime("%H:%M") #get hour data
day_formated = now.strftime("%d/%m/%Y") #get day data

"""operations_available = {
    "+": lambda a,b: (f"{a} + {b} = {a+b}"),
    "-": lambda a,b: (f"{a} - {b} = {a-b}"),
    "*": lambda a,b: (f"{a} * {b} = {a*b}"),
    "/": lambda a,b: (f"{a} / {b} = {a/b}"),
    "**": lambda a,b: (f"{a} ** {b} = {a**b}")
} #lambda for each operation type"""

calcinfos_path = "./json_files/calcinfos.json"
def main():
    user = userFunctions.WelcomeUser()
    user_datas_dict = user.copy() #copy user variable to add two new columns
    user_datas_dict.update({
        "Hours": hour_formated,
        "Day": day_formated
    })
    json_insert_data.AddToJson(user_datas_dict, "./json_files/userinfos.json")

    print(f"Welcome, Mr {user['Name']}, born in {user['Year Born']}, you receive an access to the JVBCalculator")
    

    while True:
        optionmenu = menuFunctions.menufunc()
        match optionmenu: #to avoid use if/elif/elif
            case  "1":
                try:
                    calctype = calculate_file.get_operation()
                    operation = calculate_file.get_valid_operation(calctype)
                    num1, num2 = calculate_file.get_numbers()
                    result = menuFunctions.menu[optionmenu](operation,num1,num2)
                    calcDict = {
                        "Calc Type": calctype,
                        "Operation": result,
                        "Hours": hour_formated,
                        "Day": day_formated
                        }
                    json_insert_data.AddToJson(calcDict, calcinfos_path)
                    print(f"Result: {result}")
                except ZeroDivisionError:
                    print("Division by zero is not allowed")
            case "2":
                result = menuFunctions.menu[optionmenu](user)
            case "3":
                result = menuFunctions.menu[optionmenu](calcinfos_path)
                for i in result:
                    print(i)
            case "4":
                result = menuFunctions.menu[optionmenu]()
            case "5":
                print("Goodbye! See you later!")
                break
        time.sleep(1)

main()