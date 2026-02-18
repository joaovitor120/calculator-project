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
    return user

var1 = WelcomeUser()
var2 = dict(var1)
print(type(var2))
print(type(var1))
print(var2)