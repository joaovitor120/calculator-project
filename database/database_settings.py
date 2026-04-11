import sqlite3

connection = sqlite3.connect("./database/database.db", timeout=20)
cursor = connection.cursor()
def begginer_settings():

    cursor.execute("""CREATE TABLE IF NOT EXISTS math_challenge
                (
                Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                Challenge TEXT NOT NULL,
                Result INTEGER NOT NULL,
                Hours TEXT NOT NULL,
                Day TEXT NOT NULL
                )
    """)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS User 
    (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        Year_born INTEGER NOT NULL,
        Age INTEGER NOT NULL,
        Hours TEXT NOT NULL,
        Day TEXT NOT NULL
        )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS CalcInfos 
    (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        CalcType TEXT NOT NULL,
        Operation TEXT NOT NULL,
        Hours TEXT NOT NULL,
        Day TEXT NOT NULL,
        User TEXT NOT NULL
        )
""")

def add_math_challenge_datas(challenge, result, hour, day):
    cursor.execute(f"""INSERT INTO math_challenge
                   (Challenge,Result, Hours, Day) VALUES
                   ('{challenge}', {result}, '{hour}', '{day}')
""")

def get_calculator_history(user):
    cursor.execute(f"SELECT Operation FROM CalcInfos WHERE User = '{user['Name']}'")
    result = cursor.fetchall() #[('10 ** 2 = 100',), ('20 / 2 = 10.0',)]
    return result

connection.commit()
#connection.close()