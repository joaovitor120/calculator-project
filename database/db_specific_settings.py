import sqlite3

connection = sqlite3.connect("database.db")
connection.close()
connection = sqlite3.connect("database.db")
cursor = connection.cursor()

cursor.execute("""DROP TABLE IF EXISTS math_challenge
""")