# Admin CRUD functions
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "database.db"

connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

tables = {
    "1": "CalcInfos",
    "2": "User",    
}

databases_availables = "1 - Calculation informations\n2 - User Informations"


def verify_input(user_input, options_available, input_label):
    while user_input not in options_available:
        print("Please, type a valid option.")
        user_input = input(input_label).strip()
    return user_input


def get_db_table_input():
    print(databases_availables)
    db_selected = input("Please type 1/2: ").strip()
    db_selected = verify_input(db_selected, tables.keys(), "Please type 1/2: ")
    return tables[db_selected]


def get_table_columns(table_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    table_info = cursor.fetchall()
    return [column[1] for column in table_info]


def see_datas():
    table_name = get_db_table_input()
    show_datas_from_table(table_name)


def get_record_by_id(table_name, record_id):
    cursor.execute(f"SELECT * FROM {table_name} WHERE id = ?", (record_id,))
    return cursor.fetchone()


def update_datas():
    table_name = get_db_table_input()

    show_datas_from_table(table_name)

    record_id = input("\nType the ID of the record you want to update: ").strip()

    if not record_id.isdigit():
        print("Invalid ID.")
        return

    record = get_record_by_id(table_name, record_id)

    if not record:
        print("Record not found.")
        return

    columns = get_table_columns(table_name)
    editable_columns = [column for column in columns if column != "id"]

    print("\nColumns available to update:")
    for index, column in enumerate(editable_columns, start=1):
        print(f"{index} - {column}")

    column_option = input("Choose the column number: ").strip()
    valid_options = [str(i) for i in range(1, len(editable_columns) + 1)]

    column_option = verify_input(
        column_option,
        valid_options,
        "Choose a valid column number: "
    )

    column_selected = editable_columns[int(column_option) - 1]
    new_value = input(f"Type the new value for {column_selected}: ").strip()

    confirm = input(
        f"Confirm update {column_selected} to '{new_value}'? (Y/N): "
    ).strip().upper()

    if confirm != "Y":
        print("Update canceled.")
        return

    cursor.execute(
        f"UPDATE {table_name} SET {column_selected} = ? WHERE id = ?",
        (new_value, record_id)
    )
    print(f"Rows updated: {cursor.rowcount}")
    connection.commit()

    print("Record updated successfully.")


def delete_datas():
    table_name = get_db_table_input()

    show_datas_from_table(table_name)

    record_id = input("\nType the ID of the record you want to delete: ").strip()

    if not record_id.isdigit():
        print("Invalid ID.")
        return

    record = get_record_by_id(table_name, record_id)

    if not record:
        print("Record not found.")
        return

    print(f"\nSelected record: {record}")

    confirm = input("Are you sure you want to delete this record? (Y/N): ").strip().upper()

    if confirm != "Y":
        print("Delete canceled.")
        return

    cursor.execute(f"DELETE FROM {table_name} WHERE id = ?", (record_id,))
    connection.commit()

    print("Record deleted successfully.")
    

def show_datas_from_table(table_name):
    cursor.execute(f"SELECT * FROM {table_name}")
    datas = cursor.fetchall()

    if not datas:
        print("No data found.")
        return

    columns = get_table_columns(table_name)
    print("\n" + " | ".join(columns))

    for row in datas:
        print(row)