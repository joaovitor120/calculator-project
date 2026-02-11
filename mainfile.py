import time

operations_available = {
    "+": lambda a,b: a + b,
    "-": lambda a,b: a - b,
    "*": lambda a,b: a * b,
    "/": lambda a,b: a / b 
}


def WelcomeUser():
    bdayYear = False
    year = int(input("Which year we are? "))
    bday = input("Do you already make birthiday this year?")

    if bday == "S":
        bdayYear = True
    name = input("What is your name? ")
    age = int(input("How old are you? "))
    if bdayYear == True:
        yearBorn = year - age
    else:
        yearBorn = (year - age) - 1
    User = {
        "Name": name,
        "Year Born": yearBorn,
        "Age": age
    }
    return User


def userInfo(User):
    for i in User:
        user_datas = f"{i}:{User[i]}"
        print(user_datas)

def operation(op,n1,n2):
    return operations_available[op](n1,n2)

def get_number(msg):
    while True:
        try:
            return int(input(msg))
        except ValueError:
            print("Invalid number. Try again.")

def get_user_input():
    calcType = input("Which operation do you wanna make((+)/(-)/(*)/(/))? ")
    while calcType not in operations_available:
        print("You type an invalid operation simbol.")
        calcType = input("Type which operation do you wanna make among them((+)/(-)/(*)/(/))? ")
    num1 = get_number(("Type the first number: "))
    num2 = get_number(("Type the second number: "))
    return calcType, num1, num2

def calc_process(User):
    calcType, num1, num2 = get_user_input()
    result = operation(calcType, num1, num2)
    return result

def exit_program(User):
    return "EXIT"
menu = {
    "1": calc_process,
    "2": userInfo,
    "3": exit_program
}

def menufunc():
    print("\n MENU: \n 1:Calculator \n 2:My Informations \n 3:Exit")
    optionmenu = input("Choose one of them options(1/2/3): ")
    while optionmenu not in menu:
        print("Invalid option. Please choose 1, 2, or 3.")
        optionmenu = input("Choose one of them options(1/2/3): ")
    return optionmenu


def main():
    User = WelcomeUser()
    print(f"Welcome, Mr {User['Name']}, born in {User['Year Born']}, you receive an access to the JVBCalculator")
    while True:
        
        try:
            optionmenu = menufunc()
            if optionmenu in menu:
                result = menu[optionmenu](User)
                if result != "EXIT" and optionmenu != "2":
                    print(f"Result: {result}")
        except ZeroDivisionError:
            print("Division by zero is not allowed")
        #again = input("Do you wanna continue (Y/N)? ").upper()

        if result == "EXIT":
            print("Goodbye! See you later!")
            break
        time.sleep(1)

main()