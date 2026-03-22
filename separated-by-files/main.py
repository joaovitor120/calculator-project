import time
from datetime import datetime
import user_functions
import calculate_file
import menu_functions   
from json_files import json_insert_data
import sqlite3
import uuid
from database import begginer_settings, get_calculator_history
from adm_manage import see_datas, update_datas, delete_datas

begginer_settings() # to create databases if not exists

user_id = uuid.uuid4().bytes #to be insert in sqlite
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
user_csv_path = "./csv_exported/User_data.csv"
calc_csv_path = "./csv_exported/Calc_datas.csv"

connection = sqlite3.connect("./database/database.db")
cursor = connection.cursor()
columns_user = ["Name", "Year_born", "Age", "Hours", "Day"]
columns_calc = ["CalcType", "Operation", "Hours", "Day", "User"]
tables_formatted = (", ".join(i for i in columns_user)) #to use in the sqlite command
tables_formatted_calc = (", ".join(i for i in columns_calc))



def main():
    user = user_functions.WelcomeUser()
    if user != "adm":
        adm = False
        user_datas_dict = user.copy() #copy user variable to add two new columns
        user_datas_dict.update({
            "Hours": hour_formated,
            "Day": day_formated
        })
        json_insert_data.AddToJson(user_datas_dict, "./json_files/userinfos.json")

        print(f"Welcome,{user['Name']}, born in {user['Year Born']}, you receive an access to the JVBCalculator")
        if user['New'] == True:
            cursor.execute(f"""
            INSERT INTO User
            ({tables_formatted}) VALUES
            ('{user['Name']}', {user['Year Born']}, {user['Age']}, '{hour_formated}', '{day_formated}')""")
    else:
        adm = True

    while True:
        optionmenu = menu_functions.menufunc(adm)
        if adm:
            match optionmenu:
                case "1":
                    menu_functions.menu_adm[optionmenu]()
                case "2":
                    menu_functions.menu_adm[optionmenu]()
                case "3":
                    menu_functions.menu_adm[optionmenu]()
        else:
            match optionmenu: #to avoid use if/elif/elif
                case  "1": #calculator
                    try:
                        calctype_to_verified = calculate_file.get_operation() #not verified yet
                        operation = calculate_file.get_valid_operation(calctype_to_verified)
                        num1, num2 = calculate_file.get_numbers()
                        result = menu_functions.menu[optionmenu](operation,num1,num2)
                        calcDict = {
                            "Calc Type": operation,
                            "Operation": result,
                            "Hours": hour_formated,
                            "Day": day_formated
                            }
                        #json_insert_data.AddToJson(calcDict, calcinfos_path)
                        print(f"Result: {result}")
                        cursor.execute(f"""
                        INSERT INTO CalcInfos
                        ({tables_formatted_calc}) VALUES
                        ('{calcDict["Calc Type"]}', '{calcDict["Operation"]}', '{hour_formated}', '{day_formated}', '{user['Name']}')""")
                        connection.commit()
                    except ZeroDivisionError:
                        print("Division by zero is not allowed")
                case "2": #my informations
                    result = menu_functions.menu[optionmenu](user)
                case "3": #calculator history
                    """result = menuFunctions.menu[optionmenu](calcinfos_path)
                    for i in result:
                        print(i)"""
                    result = get_calculator_history(user)
                    #cursor.execute(f"SELECT Operation FROM CalcInfos WHERE User = '{user['Name']}'")
                    #result = cursor.fetchall() #[('10 ** 2 = 100',), ('20 / 2 = 10.0',)]
                    for i in result:
                        print(str(i)[2:-3]) #to print the result without the 2 first characters and without the last 3
                case "4": #current converter
                    result = menu_functions.menu[optionmenu]()
                case "5": #math challenges
                    result = menu_functions.menu[optionmenu]()
                case "6": #export data
                    print("""1 - Export only my user datas
    2 - Export only my operations data
    3 - Export both
                        """)
                    select_option = input("Please, type 1, 2 or 3 to choose one export option: ").split()
                    def user_to_csv():
                        user_datas_to_csv = {}
                        for i in user_datas_dict:
                            user_datas_to_csv[i] = [f'{user_datas_dict[i]}']
                            
                            return user_datas_to_csv
                    def calc_to_csv():
                        cursor.execute(f"SELECT CalcType, Operation FROM CalcInfos WHERE User = '{user['Name']}'")
                        calc_history = cursor.fetchall()
                        calc_history_to_csv = {"CalcType": [],
                    "Operation": []}
                        for i in calc_history:
                            calc_history_to_csv["CalcType"].append(i[0])
                            calc_history_to_csv["Operation"].append(i[1][2:-3]) 
                        return calc_history_to_csv
                    match select_option:
                        case "1":
                            user_datas_to_csv = user_to_csv()
                            menu_functions.menu[optionmenu](user_datas_to_csv, user_csv_path)
                        case "2": 
                            calc_history_to_csv = calc_to_csv() 
                            menu_functions.menu[optionmenu](calc_history_to_csv, calc_csv_path)
                        case "3":
                            user_datas_to_csv = user_to_csv()
                            calc_history_to_csv = calc_to_csv() 
                            menu_functions.menu[optionmenu](user_datas_to_csv, user_csv_path)
                            menu_functions.menu[optionmenu](calc_history_to_csv, calc_csv_path)
                case "7": #exit
                    print("Goodbye! See you later!")
                    connection.commit() #to save db changes on db
                    connection.close()
                    break
        time.sleep(1)

main()

