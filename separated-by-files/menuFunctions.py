import calculate_file
import calculate_file
import userFunctions
import userFunctions
import json
import get_exchange_rate

def exit_program(user,op,n1,n2): #this function was created to set a flag when the users want to get out
    return "EXIT"

def calcinfo(file):
    with open(file, "r") as f:
        content = f.read().strip()
        content_decoded = json.loads(content)
        operationsHistory = []
        for i in content_decoded:
            operationsHistory.append(i['Operation'])
        return operationsHistory
    
    

menu = { #dict with functions inserted
    "1": calculate_file.calculate,
    "2": userFunctions.show_user_data,
    "3": calcinfo,
    "4": get_exchange_rate.proccess_main,
    "5": exit_program
}

def menufunc():
    print("\n MENU: \n 1:Calculator \n 2:My Informations \n 3:Calculator History \n 4:Currency converter \n 5:Exit")
    optionmenu = input("Choose one of them options(1/2/3/4/5): ")
    while optionmenu not in menu:
        print("Invalid option. Please choose 1, 2, 3, 4 or 5.")
        optionmenu = input("Choose one of them options(1/2/3/4/5): \n ")
    return optionmenu

