import sqlite3

db = "./database/database.db"
connection = sqlite3.connect(db)
cursor = connection.cursor()

#cursor.execute("""
#DELETE FROM User WHERE id = 2
#""")

cursor.execute(f"SELECT CalcType, Operation FROM CalcInfos WHERE User = 'joaovitor'")
calc_history = cursor.fetchall()
calc_history_to_csv = {"CalcType": [],
                       "Operation": []}
for i in calc_history:
    calc_history_to_csv["CalcType"].append(i[0])
    calc_history_to_csv["Operation"].append(i[1][2:-3])   
print(calc_history_to_csv)
#connection.commit()
