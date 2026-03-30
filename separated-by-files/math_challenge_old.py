import random
from sympy import isprime
import time
 
levels = [1,2,3,4]
calc_types = [1,2]
operations_type = {
    "+": lambda a,b: a + b,
    "-": lambda a,b: a - b,
    "*": lambda a,b: a * b,
    "/": lambda a,b: a / b,
    "**": lambda a,b: a ** b
}

length_op_list = len(list(operations_type.keys()))

class DifficultyRange:
    def __init__(self):
        self.ranges = {
            "easy": {"min": 2, "med": 10, "max": 20},
            "medium": {"min": 11, "med": 20, "max": 50},
            "hard": {"min": 21, "med": 30, "max": 80},
            "very hard": {"min": 31, "med": 40, "max": 100}
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
index_easy_list = ranges.get_all("easy")
index_medium_list = ranges.get_all("medium")
index_hard_list = ranges.get_all("hard")
index_veryhard_list = ranges.get_all("very hard")

def get_level_difficult():

    print("""1 - Simple operations(with only two numbers)
2 - Complex operations(with more than two numbers)
""")
    calc_type_complex = int(input("Choose one operation among them(1/2) to continue: "))
    if calc_type_complex not in calc_types:
        calc_type_complex = int(input("Choose 1 or 2 to continue, please: "))
    print("""1 - Easy
2 - Medium
3 - Hard
4 - Very Hard
""")
    level_difficult = int(input("Choose one level difficult among them(1/2/3/4): "))
    if level_difficult not in levels:
        level_difficult = int(input("Choose a number between 1 and 4, please: "))
    return calc_type_complex, level_difficult

def select_random_non_prime(range_min, range_max):
    """Select a random non-prime number within a given range."""
    # Create a list of all non-prime numbers in the range
    non_primes = [n for n in range(range_min, range_max) if not isprime(n)]    
    if non_primes == []:
        return random.randint(range_min, range_max)
    else:
        # Select a random non-prime from the list using the random.choice function
        return random.choice(non_primes)

def get_calculator_datas(range_min, range_med, 
                         range_max, index_min, index_max):
    num1 = select_random_non_prime(range_med,range_max)
    if range_min > 10 and range_med > 20:
        range_min = int(range_min // 2.3)
        range_med = int(range_med // 2)
    num2 = select_random_non_prime(range_min,range_med)
    op_symbol = random.choice((list(operations_type.keys()))[index_min:index_max])
    return num1, num2, op_symbol

def verify_numbers(result, num1,num2, op_symbol,
                   index_min, index_med, index_max, 
                   op_index_min, op_index_max):
    if isinstance(result, int) == False:
        numbers = list(range(index_min, index_med))
        non_prime_numbers_for_divide = [i for i in numbers if i % 2 == 0]
        for _ in range(10):
            num2 = random.randint(index_min,index_med)
            result = operations_type[op_symbol](num1, num2)
            if isinstance(result, int):
                break
        while isinstance(result, int) == False:
            op_symbol = random.choice((list(operations_type.keys()))[op_index_min:op_index_max])
            result = operations_type[op_symbol](num1, num2)
    if op_symbol == "**" and num2 != 2:
        num1 = select_random_non_prime(int(index_med // 2.5),int(index_max // 3))
        num2 = 2
        result = operations_type[op_symbol](num1, num2)

    return num1, num2, op_symbol, result

def answer_check_loop(num1,num2, op_symbol,
                      result_calc, result, 
                      multiple_operations=False):
    while result_calc != result:
        print("Wrong answer, try again: ")
        if multiple_operations:
            result_calc = int(input(multiple_operations))
        else:
            result_calc = int(input(f"{num1} {op_symbol} {num2} = "))
def generate_challenge(difficulty, op_min, op_max):
    num1, num2, op_symbol = get_calculator_datas(ranges.get_min(difficulty), ranges.get_med(difficulty), 
                                                 ranges.get_max(difficulty),op_min,op_max)
    result = operations_type[op_symbol](num1, num2)
    num1, num2, op_symbol, result = verify_numbers(result,num1,num2,op_symbol,ranges.get_min(difficulty), ranges.get_med(difficulty), ranges.get_max(difficulty),op_min,op_max)
    return num1, num2, op_symbol, result
def challenge_simple(difficulty, op_min, op_max):
    num1, num2, op_symbol, result = generate_challenge(difficulty, op_min, op_max)
    start_time = time.perf_counter()  
    result_calc = int(input(f"{num1} {op_symbol} {num2} = "))
    if result_calc != result:
        answer_check_loop(num1,num2,op_symbol,result_calc,result)                    
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print(f"Perfect, your answer the correct answer in {int(execution_time)} seconds, congratulations!")
    
def challenge_complex(difficulty, op_min, op_max):
    num1, num2, op_symbol, result = generate_challenge(difficulty, op_min, op_max)
                    
    num3, num4, op_symbol_1, result_1 = generate_challenge(difficulty, op_min, op_max)
    op_last_calc = op_max - 1 if op_max == length_op_list else op_max
    op_symbol_2 = random.choice((list(operations_type.keys()))[op_min:op_last_calc])
    print(op_symbol_2)
    final_result = operations_type[op_symbol_2](result, result_1)
    result, result_1, op_symbol_2, final_result = verify_numbers(final_result,result,result_1,op_symbol_2,ranges.get_min(difficulty), ranges.get_med(difficulty), ranges.get_max(difficulty),op_min, op_max)
    print(op_symbol_2)
    if op_symbol_2 == "**":
        op_symbol_2 = random.choice((list(operations_type.keys()))[op_min:4])
        final_result = operations_type[op_symbol_2](result, result_1)
    expression = f"({num1} {op_symbol} {num2}) {op_symbol_2} ({num3} {op_symbol_1} {num4}) = "

    start_time = time.perf_counter()                            
    result_calc = int(input(expression))
    if result_calc != final_result:
        answer_check_loop(result,result_1,op_symbol_2,result_calc,final_result,expression) 
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print(f"Perfect, your answer the correct answer in {int(execution_time)} seconds, congratulations!") 

def math_challenges():
    calc_type_complex, difficult = get_level_difficult()
    difficulty_map = {1: "easy", 2: "medium", 3: "hard", 4: "very hard"}
    op_index = {
        'easy': (0,4),
        'medium': (2,4),
        'hard': (3, length_op_list),
        'very hard': (3, length_op_list)
    }
    op_min, op_max = op_index[difficulty_map[difficult]]
    match calc_type_complex:
        case 1:
            match difficult:
                case 1:                 
                    challenge_simple(difficulty_map[difficult], op_min, op_max)
                case 2:
                    challenge_simple(difficulty_map[difficult], op_min, op_max)
                case 3:
                    challenge_simple(difficulty_map[difficult], op_min, op_max)
                case 4:
                    challenge_simple(difficulty_map[difficult], op_min, op_max)
        case 2:
            match difficult:
                case 1:
                    challenge_complex(difficulty_map[difficult], op_min, op_max)
                case 2:
                    challenge_complex(difficulty_map[difficult], op_min, op_max)
                case 3:
                    challenge_complex(difficulty_map[difficult], op_min, op_max)
                case 4:
                    challenge_complex(difficulty_map[difficult], op_min, op_max)

#separate functions that make more than one function

math_challenges()