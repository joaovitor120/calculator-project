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
    return name, yearBorn, year, age

name, yearBorn, year, age = WelcomeUser()
print(f"Welcome, Mr {name}, born in {yearBorn}, you receive an access to the JVBCalculator")

def userInfo():
    infos = {
        "Name": name,
        "Year Born": yearBorn,
        "Age": age
    }
    for i in infos:
        print(f"{i}:{infos[i]}")

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

def calc_process():
    calcType, num1, num2 = get_user_input()
    result = operation(calcType, num1, num2)
    return result
get_out = {
    "exit": False
}
menu = {
    "1": calc_process,
    "2": userInfo,
    "3": lambda: get_out.update({"exit": True})
}

def menufunc():
    print(" 1:Calculator \n 2:My Informations \n 3:Exit")
    optionmenu = input("Choose one of them options(1/2/3): ")
    while optionmenu not in menu:
        print("Invalid option. Please choose 1, 2, or 3.")
        optionmenu = input("Choose one of them options(1/2/3): ")
    return optionmenu


def main():

    while True:
        try:
            optionmenu = menufunc()
            if optionmenu in menu:
                result = menu[optionmenu]()
                if result is not None:
                    print(f"Result: {result}")
        except ZeroDivisionError:
            print("Division by zero is not allowed")
        #again = input("Do you wanna continue (Y/N)? ").upper()

        if get_out["exit"] == True:
            print("Goodbye! See you later!")
            break

main()