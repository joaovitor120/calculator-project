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
def get_db_table_input():
    print(databases_availables)
    db_selected_by_user = input()
    db_selected_by_user = input_verified(db_selected_by_user, options_available, input_label)
    return int(db_selected_by_user)

def get_table_columns(table_name):
    columns = []
    cursor.execute(f"PRAGMA table_info('{table_name}')") #see CalcInfos informations
    table_info = cursor.fetchall()
    for column_info in table_info:
        column = column_info[1]
        columns.append(column)
    return columns #return a dict 
    
def see_datas(): #see datas on the database
    db = get_db_table_input()
    cursor.execute(f"SELECT * FROM {tables[db - 1]}")
    datas = cursor.fetchall() #touple
    for i in datas:
        print(i)
        
def update_datas(): #update datas on the database
    print("These are the columns at CalcInfos:")
    columns = get_table_columns("CalcInfos")
    index_columns = [str(i+1) for i, x in enumerate(columns)]
    i = 0
    for column in columns:
        print(f"{column}({i+1})")
        i+=1
    column_selected_label = "Which column do you want to update:"
    column_selected_input = input(column_selected_label)
    column_selected = input_verified(column_selected_input, (columns + index_columns), column_selected_label)

    if column_selected in index_columns:
        column_selected = columns[(int(column_selected) - 1)]
    print("\n" + f"lines FROM column {column_selected}: ")
    cursor.execute(f"SELECT {column_selected} FROM CalcInfos")
    lines = cursor.fetchall()
    i = 1
    lines_qtd = []
    for line in lines:
        print(f"{i} - {line}")
        lines_qtd.append(str(i))
        i+=1
    print("\n")
    line_selected_label = (f"Type the line do you want to update {((str(lines_qtd)).replace("[", "(").replace("]", ")"))}: ")
    line_selected = input(line_selected_label)
    line_selected = input_verified(line_selected, lines_qtd, line_selected_label)
    #continue here implementing the update function
    
def delete_datas(): #delete datas on the database
    pass

