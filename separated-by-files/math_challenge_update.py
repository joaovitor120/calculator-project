import random
import time
import math
from database import add_math_challenge_datas
from datetime import datetime


now = datetime.now()
hour_formated = now.strftime("%H:%M") #get hour data
day_formated = now.strftime("%d/%m/%Y") #get day data
levels = ['1','2','3','4']
levels_qtd = len(levels)
calc_types = ['1','2']

operations_type = {
    "+": lambda a,b: a + b,
    "-": lambda a,b: a - b,
    "*": lambda a,b: a * b,
    "/": lambda a,b: a / b,
    "**": lambda a,b: a ** b
}

operations_list = list(operations_type.keys())
operations_list_length = len(operations_list)

op_index = {
    'easy': (0,3), #(+, -, /, *) --> it will be used in random, that excludes one the last op_symbol
    'medium': (2,4), #(*,/)
    'hard': (2, (operations_list_length)), #(*, /)
    'very hard': (2, (operations_list_length + 1)) #(*, /, **)
}

difficulty_map = {'1': "easy", '2': "medium", '3': "hard", '4': "very hard"}

def isprime(num):
    if num < 2:
        return False
    for i in range(2, (int(math.sqrt(num))) + 1): #i dont't need to analyse all the divisors to see if the num is prime, because the max pair i will have will stay in this range
        if num % i == 0:
            return False
    return True

class DifficultyRange: #to set each calculation range
    def __init__(self):
        self.ranges = {
            "easy": {"min": 2, "med": 11, "max": 21},
            "medium": {"min": 10, "med": 21, "max": 51},
            "hard": {"min": 20, "med": 31, "max": 81},
            "very hard": {"min": 30, "med": 41, "max": 101}
        }
    
    def get_min(self, difficulty):
        return self.ranges[difficulty]["min"]
    
    def get_med(self, difficulty):
        return self.ranges[difficulty]["med"]
    
    def get_max(self, difficulty):
        return self.ranges[difficulty]["max"]
    def get_all(self, difficulty):
        return self.ranges[difficulty]
    
ranges = DifficultyRange()
ranges_min = ranges.get_min
ranges_med = ranges.get_med
ranges_max = ranges.get_max
"""index_easy_list = ranges.get_all("easy")
index_medium_list = ranges.get_all("medium")
index_hard_list = ranges.get_all("hard")
index_veryhard_list = ranges.get_all("very hard")"""

"""def isprime(num):
    divisors = []
    for i in range(1, num+1):
        if num % i == 0:
            divisors.append(i)
    if len(divisors) == 2:
        return True
    else:
        return False"""

def ensure_option_menu_correctly(user_input,message_input,options_available): #ensure a valid input
    options_available_to_use = ('/'.join (i for i in options_available))
    while user_input not in options_available:
        print(f"This option is not available, please choose one option among them({options_available_to_use}) ")
        user_input = input(message_input)
    return user_input

def get_levels_difficulty(): #get inputs
    print("""1 - Simple operations(with only two numbers)
2 - Complex operations(with more than two numbers)
""")   

    message_input_calc_complex = "Choose one operation among them(1/2) to continue: "
    calculation_complexity_input = input(message_input_calc_complex).strip()
    options_available_calc = ['1', '2']
    calculation_complexity = ensure_option_menu_correctly(calculation_complexity_input, message_input_calc_complex, options_available_calc)
    print("""1 - Easy
2 - Medium
3 - Hard
4 - Very Hard
""")
    options_available_level = ['1', '2', '3', '4']
    level_difficult_message = "Choose one level difficult among them(1/2/3/4): "
    level_difficult_input = input(level_difficult_message).strip()
    level_difficult = ensure_option_menu_correctly(level_difficult_input, level_difficult_message, options_available_level)
    return calculation_complexity, level_difficult


def select_random_non_prime(range_min, range_max):
    """Select a random non-prime number within a given range."""
    # Create a list of all non-prime numbers in the range
    non_primes = [n for n in range(range_min, range_max) if not isprime(n)]    
    if non_primes == []:
        return random.randint(range_min, range_max)
    else:
        # Select a random non-prime from the list using the random.choice function
        return random.choice(non_primes)

def get_calculator_datas(range_min, range_med, range_max, index_min, index_max):
    num1 = select_random_non_prime(range_med,range_max)
    if range_min > 10 and range_med > 20:
        range_min = int(range_min // 2)
        range_med = int(range_med // 2)
    num2 = select_random_non_prime(range_min,range_med)
    op_symbol = random.choice((operations_list)[index_min:index_max])
    return num1, num2, op_symbol

def ensure_integer_result_simple(result, num1,num2, op_symbol,index_min, index_med, op_index_min, op_index_max):
    if not isinstance(result, int): #if result not int
        numbers = list(range(index_min, index_med))
        if op_symbol == "/":
            validates_num2 = [i for i in numbers if num1 % i == 0]
            if validates_num2:
                num2 = random.choice(validates_num2)
                result = operations_type[op_symbol](num1,num2)
            else: #if not numbers options for num2 --> choose another op_symbol and num2
                while isinstance(result, int) == False:  #isistance return only True or False
                    op_symbol = random.choice((operations_list)[op_index_min:op_index_max])
                    result = operations_type[op_symbol](num1, num2)
                    if isinstance(result, int):
                        break
                    else:
                        num2_options = [i for i in numbers if isinstance((operations_type[op_symbol](num1, i)), int)]
                        if num2_options:
                            num2 = random.choice(num2_options)
                            result = operations_type[op_symbol](num1, num2)
    return num2, op_symbol, result

def force_expoent_two(result, num1,num2,op_symbol, index_med, index_max):
        if op_symbol == "**" and num2 != 2:
            num1 = select_random_non_prime(int(index_med // 2.5),int(index_max // 3)) #ensure the number is less than 33
            num2 = 2
            result = operations_type[op_symbol](num1, num2)
        return num1,num2,result
def validate_calculation(answer, correct_answer):
    if int(answer) == int(correct_answer):
        return True #use this text to continue the proccess
    else:
        return False #use this flag to get a new input 
    
def answer_retry_loop(num1,num2, op_symbol,user_result_answer, result, multiple_operations=False):
    answer_status = validate_calculation(user_result_answer, result)
    while answer_status == False:
        print("Wrong answer, try again: ")
        if multiple_operations:
            try:
                user_result_answer = int(input(multiple_operations))
            except ValueError:
                print("Please, type an integer value: ")
        else:
            user_result_answer = int(input(f"{num1} {op_symbol} {num2} = "))
        answer_status = validate_calculation(user_result_answer, result)

def generate_challenge(difficulty, op_min, op_max, last_num=False):
    if last_num:
        num1, num2, op_symbol = get_calculator_datas(ranges_min(difficulty), ranges_med(difficulty), ranges_max(difficulty),op_min,op_max - 1)
    else:
        num1, num2, op_symbol = get_calculator_datas(ranges_min(difficulty), ranges_med(difficulty), ranges_max(difficulty),op_min,op_max)
    result = operations_type[op_symbol](num1, num2)
    num2, op_symbol, result = ensure_integer_result_simple(result,num1,num2,op_symbol,ranges_min(difficulty), ranges_med(difficulty),op_min,op_max)
    num1, num2, result = force_expoent_two(result, num1,num2,op_symbol, ranges_med(difficulty), ranges_max(difficulty))
    return num1, num2, op_symbol, result

def init_timer():
    start_time = time.perf_counter()  
    return start_time
def end_timer():
    end_time = time.perf_counter()
    return end_time

def ask_question(num1=None,num2=None,op_symbol=None, expression=None): #i used each paramater as None to make them optional
    if expression:
        try:
            user_result_answer = int(input(expression))
        except Exception as e:
            print(f"Error, {e}")
    else:
        user_result_answer = int(input(f"{num1} {op_symbol} {num2} = "))
    return user_result_answer

def challenge_simple(difficulty, op_min, op_max):
    num1, num2, op_symbol, final_result = generate_challenge(difficulty, op_min, op_max)
    start_time = init_timer()
    user_result_answer = ask_question(num1,num2,op_symbol)
    expression = f"{num1} {op_symbol} {num2}"
    answer_retry_loop(num1,num2,op_symbol,user_result_answer,final_result)                    
    end_time = end_timer()
    execution_time = end_time - start_time
    print(f"Perfect, you answered correctly in {int(execution_time)} seconds, congratulations!")
    add_math_challenge_datas(expression, final_result, hour_formated, day_formated)
def challenge_complex(difficulty, op_min, op_max):
    num1, num2, op_symbol, result_0 = generate_challenge(difficulty, op_min, op_max)
                    
    num3, num4, op_symbol_1, result_1 = generate_challenge(difficulty, op_min, op_max, last_num=True)

    if op_max == operations_list_length-1:
        op_symbol_2 = random.choice((operations_list)[op_min:op_max-1])
    else:
        op_symbol_2 = random.choice((operations_list)[op_min:op_max])
    #print(op_symbol_2)
    final_result = operations_type[op_symbol_2](result_0, result_1)
    result_1, op_symbol_2, final_result = ensure_integer_result_simple(final_result,result_0,result_1,op_symbol_2,ranges_min(difficulty), ranges_med(difficulty),op_min, op_max)
    #print(op_symbol_2)
    expression = f"({num1} {op_symbol} {num2}) {op_symbol_2} ({num3} {op_symbol_1} {num4}) = "

    start_time = init_timer()                           
    user_result_answer = ask_question(expression=expression) #only to get the user input for the expression
    answer_retry_loop(result_0,result_1,op_symbol_2,user_result_answer,final_result,expression) 
    end_time = end_timer()
    execution_time = end_time - start_time
    print(f"Perfect, your answer correctly in {int(execution_time)} seconds, congratulations!") 
    add_math_challenge_datas(expression, final_result, hour_formated, day_formated)

def math_challenges():
    running = True
    print("Welcome to the Mental Math Challenge! Here you will practice your mental math skills by answering with integers only. \n")
    while running == True:
        
        calc_type_complex, difficult = get_levels_difficulty()
        
        op_min, op_max = op_index[difficulty_map[difficult]]
        if calc_type_complex == '1':                                
                challenge_simple(difficulty_map[difficult], op_min, op_max)

                
        if calc_type_complex == '2':
                challenge_complex(difficulty_map[difficult], op_min, op_max)
        return_to_menu_msg = 'Do you want to return to main menu to execute another functions(Y/N)? '
        return_to_menu_input = input(return_to_menu_msg).upper().strip()
        return_to_menu_msg_options = ['Y', 'N']
        return_to_menu = ensure_option_menu_correctly(return_to_menu_input, return_to_menu_msg, return_to_menu_msg_options).upper().strip()
        if return_to_menu == 'Y':
            running = False
#separate functions that make more than one function
