operations_available = {
    "+": lambda a,b: (f"{a} + {b} = {a+b}"),
    "-": lambda a,b: (f"{a} - {b} = {a-b}"),
    "*": lambda a,b: (f"{a} * {b} = {a*b}"),
    "/": lambda a,b: (f"{a} / {b} = {round(a/b, 2)}") ,
    "**": lambda a,b: (f"{a} ** {b} = {a**b}")
} #lambda for each operation type

operations = (" ".join([str(f'{i}') for i in operations_available]))

#function output
def operation(op,n1,n2):
    return operations_available[op](n1,n2) #use the dict with lambdas to execute each operations

def validate_number(msg): #number validate, to see if the number is an integer
    while True: 
        try:
            return int(input(msg)) #for now only accept int values from input
        except ValueError: #if number insert not an integer type
            print("Invalid number. Try again.")
def get_valid_operation(operation): #operation verification, i only want operations inputs availables
        while operation not in operations_available: #if the operations type not is includede in operations available dict
            print(f"Invalid operation, select only one of them:{operations}")
            operation = input(f"Which operation do you wanna make{operations}? ").strip() #strip to remove blank spaces
        return operation # when it get out loop
            
            
def get_operation(): #get input operation
    return input(f"Which operation do you wanna make ({operations})? ").strip() #strip to remove blank spaces

def get_numbers(): #input function
    num1 = validate_number(("Type the first number: "))
    num2 = validate_number(("Type the second number: "))
    return num1, num2
def calculate(op,n1,n2):#executable function
    result = operation(op, n1, n2)
    return result