#here i will have some adm's functions
import sqlite3

connection = sqlite3.connect("./database/database.db")
cursor = connection.cursor()
tables = ["CalcInfos", "User"]
options_available = ['1', '2']
databases_availables = ("1 - Calculation informations \n2 - User Informations")
input_label = ("Please type 1/2: ")


def input_verified(user_input, options_available, input_label):
    while user_input not in options_available: #only accepted 1/2 options
        print(f"Please, type a valid option.")
        user_input = input(input_label)
    return user_input
def get_db_input():
    print(databases_availables)
    db_selected_by_user = input()
    db_selected_by_user = input_verified(db_selected_by_user, options_available, input_label)
    return int(db_selected_by_user)
def see_datas(): #see datas on the database
    db = get_db_input()
    cursor.execute(f"SELECT * FROM {tables[db - 1]}")
    datas = cursor.fetchall() #touple
    for i in datas:
        print(i)
def update_datas(): #update datas on the database
    pass
def delete_datas(): #delete datas on the database
    pass