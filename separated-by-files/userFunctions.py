#function input --> get datas from user
def WelcomeUser():
    bdayYear = False
    year = int(input("Which year we are? "))
    bday = input("Do you already make birthiday this year?(Y/N)").upper()

    if bday == "Y":
        bdayYear = True
    name = input("What is your name? ")
    age = int(input("How old are you? "))
    yearBorn = year - age - (0 if bdayYear else 1) #remove 1 year from year born if already make birthday or 0 if not
    user = {
        "Name": name,
        "Year Born": yearBorn,
        "Age": age
    }
    return user #return a dict with all user info

#function output
def show_user_data(user):
    for i in user:
        user_datas = f"{i}:{user[i]}" #to show userdatas more friendly in print
        print(user_datas)