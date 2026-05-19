#here i will have some adm's functions
import sqlite3

connection = sqlite3.connect("database/database.db")
cursor = connection.cursor()
tables = ["CalcInfos", "User"]
options_available = ['1', '2']
databases_availables = ("1 - Calculation informations \n2 - User Informations")
input_label = ("Please type 1/2: ")

def verify_input(user_input, options_available, input_label):
    while user_input not in options_available: #only accepted 1/2 options
        print(f"Please, type a valid option.")
        user_input = input(input_label)
    return user_input
def get_db_table_input():
    print(databases_availables)
    db_selected_by_user = input()
    db_selected_by_user = verify_input(db_selected_by_user, options_available, input_label)
    return int(db_selected_by_user)

def get_table_columns(table_name):
    columns = []
    cursor.execute(f"PRAGMA table_info('{table_name}')") #see CalcInfos informations
    table_info = cursor.fetchall()
    for column_info in table_info:
        column = column_info[1]
        columns.append(column)
    return columns #return a list 

def get_line_type(table_name, line):
    column_type = ''
    cursor.execute(f"PRAGMA table_info('{table_name}')") #see CalcInfos informations
    table_info = cursor.fetchall()
    i = 1
    for column_info in table_info:
        if i == line:
            column_type = column_info[2]
            return column_type
        else:
            pass
        i+=1

def get_new_value(value_type):
    new_value = input("Type the new value do you want do update: ")
    return value_type(new_value)
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
    column_selected = verify_input(column_selected_input, (columns + index_columns), column_selected_label)

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
    #line_selected_label = (f"Type the line do you want to update {((str(lines_qtd)).replace("[", "(").replace("]", ")"))}: ")
    line_selected_label1 = ("Which line do you want to update? ")
    line_selected = input(line_selected_label1)
    line_selected = verify_input(line_selected, lines_qtd, line_selected_label1)
    line_type = get_line_type('CalcInfos', int(column_selected))
    print(line_type)#with problem, fix that
    #continue here implementing the update function
    
def delete_datas(): #delete datas on the database
    pass