from core import calculate_file as calculate_file
from core import user
from features import get_exchange_rate
from features import export_data
import json
from features.math_challenge_update import math_challenges
from database.adm_manage import see_datas, update_datas, delete_datas

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
    "2": user.show_user_data,
    "3": calcinfo,
    "4": get_exchange_rate.proccess_main,
    "5": math_challenges,
    "6": export_data.to_csv,
    "7": exit_program,
}
menu_adm = {
    "1": see_datas,
    "2": update_datas,
    "3": delete_datas,
    "4": exit_program
}

def menufunc(adm=False):
    if adm:
        print(F"\n ADM MENU: \n 1: See datas on the databases \n 2: Update some data on the database \n 3: Delete some data on the databases \n 4: Exit \n")
        optionmenu = input("Choose one of them options(1/2/3/4): ")
        while optionmenu not in menu_adm:
            print("Invalid option. Please choose 1, 2, 3, 4")
            optionmenu = input("Choose one of them options(1/2/3/4): ")
    else:
        print("\n MENU: \n 1:Calculator \n 2:My Informations \n 3:Calculator History \n 4:Currency converter \n 5:Mental Math Challenge \n 6:Export data \n 7:Exit \n")
        optionmenu = input("Choose one of them options(1/2/3/4/5/6/7): ")
        while optionmenu not in menu:
            print("Invalid option. Please choose 1, 2, 3, 4, 5, 6 or 7.")
            optionmenu = input("Choose one of them options(1/2/3/4/5/6/7): ")
    return optionmenu
