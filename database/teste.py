import sqlite3

connection = sqlite3.connect("./database.db")
cursor = connection.cursor()
tables = ["CalcInfos", "User"]
options_available = ['1', '2']
databases_availables = ("1 - Calculation informations \n2 - User Informations")
input_label = ("Please type 1/2: ")

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

column_type = ''
cursor.execute(f"PRAGMA table_info('CalcInfos')")
table_info = cursor.fetchall()
i = 1
line = 1
for column_info in table_info:
    if i == line:
        column_type = column_info[2]
    else:
        pass
print(column_type)