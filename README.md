# 🚀 JVBCalculator

> A modern, modular, and extensible Python calculator — designed not just for basic operations, but to simulate patterns and features commonly found in real-world applications.

After a break from Python, I returned by building this project as a hands-on exercise in clean code principles. It goes beyond a simple calculator by integrating **API consumption, data persistence, user authentication, and structured program design**.

---

## Table of Contents

1. [Features](#features)
2. [Architecture & File Structure](#architecture--file-structure)
3. [Tech Stack](#tech-stack)
4. [Key Technical Decisions](#key-technical-decisions)
5. [How to Run](#how-to-run)
6. [Usage Examples](#usage-examples)
7. [What This Project Demonstrates](#what-this-project-demonstrates)

---

## Features

### 🔐 User Authentication System

**File:** `user.py`

The system distinguishes two scenarios at startup:

- **New user:** collects a unique username (verified against the database), age, and whether the user has already had their birthday this year. This last piece of information is used to precisely calculate the birth year:

```python
yearBorn = year - age - (0 if bdayYear else 1)
```

This avoids the common mistake of simply subtracting age from the current year — someone who hasn't had their birthday yet was technically born in a different year than someone who has.

- **Returning user:** looks up the username in the database and retrieves stored data. Typing `adm` as the username redirects to the admin panel after password validation.

Registered usernames are loaded into memory at startup (`NamesList`) for instant availability checks, without needing a database query on every attempt.

---

### 🔢 Calculator with 5 Operations

**File:** `calculate_file.py`

Operations available: addition (`+`), subtraction (`-`), multiplication (`*`), division (`/`), and exponentiation (`**`).

The implementation uses a **dictionary of lambdas** to map each operation symbol to its corresponding function, avoiding a long `if/elif` chain:

```python
operations_available = {
    "+":  lambda a, b: (f"{a} + {b} = {a+b}"),
    "-":  lambda a, b: (f"{a} - {b} = {a-b}"),
    "*":  lambda a, b: (f"{a} * {b} = {a*b}"),
    "/":  lambda a, b: (f"{a} / {b} = {round(a/b, 2)}"),
    "**": lambda a, b: (f"{a} ** {b} = {a**b}")
}
```

Input goes through two separate validation stages: `get_operation()` captures the raw input, and `get_valid_operation()` checks whether it belongs to the accepted set, looping until valid. Numbers are also validated with `ValueError` handling to ensure only integers are accepted.

Every calculated operation is saved to the database with the operation type, formatted result, timestamp, and the logged-in username.

---

### 📜 Operation History

**File:** `main.py` — case `"3"`, integrated with `database.py`

History is retrieved directly from SQLite filtered by the logged-in username. Results come back as a list of tuples in the format `('result',)`, so a slice `str(i)[2:-3]` is used to extract only the clean content before displaying it.

---

### 🌐 Real-Time Currency Converter

**File:** `get_exchange_rate.py`

Makes HTTP requests to the AwesomeAPI public endpoint (`economia.awesomeapi.com.br`) to fetch live exchange rates for USD, EUR, and BTC against the Brazilian Real (BRL).

```python
url = "https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL"
response = requests.get(url)
exchange_rate = response.json()[f"{coin_code}{codein}"]['bid']
```

The module separates input collection (`get_input_coin`), the conversion math (`convertion_coin`), and the main flow (`proccess_main`), following the single responsibility principle.

---

### 🧠 Mental Math Challenges

**File:** `math_challenge_update.py`

The most complex feature of the project. Generates random math challenges with:

**Two modes:**
- Simple: two numbers and one operator (`num1 op num2`)
- Complex: two expressions in parentheses connected by a central operator (`(a op b) op (c op d)`)

**Four difficulty levels** with increasing numeric ranges:

| Level | Min | Med | Max | Available Operations |
|-------|-----|-----|-----|----------------------|
| Easy | 2 | 11 | 21 | `+`, `-`, `*`, `/` |
| Medium | 10 | 21 | 51 | `*`, `/` |
| Hard | 20 | 31 | 81 | `*`, `/`, `**` |
| Very Hard | 30 | 41 | 101 | `*`, `/`, `**` |

**Integer result guarantee:** the `ensure_integer_result_simple()` function ensures the expected answer is always a whole number — essential since the challenge is mental math. When division doesn't produce an integer, the system swaps operators or adjusts operands automatically.

**Primality check:** the `isprime()` function uses the square root algorithm to identify prime numbers. Generated challenge numbers preferentially avoid primes (via `select_random_non_prime`), making multiplications and divisions produce cleaner results:

```python
def isprime(num):
    if num < 2:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True
```

**Response timer:** answer time is measured with `time.perf_counter()` (more precise than `time.time()`) and shown to the user at the end of each challenge.

The `DifficultyRange` class encapsulates numeric ranges per level, providing `get_min`, `get_med`, `get_max`, and `get_all` methods for organized access to each difficulty configuration.

---

### 📊 Data Export to CSV

**Files:** `export_data.py`, integrated in `main.py`

The system allows exporting three combinations:
- User data only (name, age, birth year, access timestamp)
- Operation history only (operation type and result)
- Both simultaneously

Uses the `pandas` library to create DataFrames and export to `.csv`. If the file already exists at the target path, it is removed before recreating to avoid corrupt or overlapping files.

---

### 🛠️ Admin Panel

**File:** `adm_manage.py`

Accessible by typing `adm` as the username and providing the master password. Presents a separate menu with direct database access:

- `see_datas()` — lists all records from a selected table
- `update_datas()` — planned for record editing (upcoming)
- `delete_datas()` — planned for record removal (upcoming)

The admin menu is completely separate from the regular user menu, including its own `menu_adm` dictionary in `menu_functions.py`.

---

## Architecture & File Structure

```
JVBCalculator/
│
├── main.py                  # Entry point. Orchestrates the main flow,
│                              manages the menu loop, SQLite connection,
│                              and integration between all modules.
│
├── user.py                  # User authentication and registration.
│                              Loads users from the database at startup.
│                              Functions: WelcomeUser(), show_user_data()
│
├── calculate_file.py        # Calculation logic.
│                              Lambda dictionary per operation.
│                              Functions: calculate(), get_operation(),
│                              get_valid_operation(), get_numbers()
│
├── menu_functions.py        # Centralizes menus as dictionaries.
│                              Maps each option to its handler function.
│                              Menus: menu (user), menu_adm (admin)
│
├── math_challenge_update.py # Mental math challenge engine.
│                              Random expression generation, integer result
│                              validation, timer, and difficulty levels.
│
├── get_exchange_rate.py     # Currency API integration.
│                              Converts USD/EUR/BTC to BRL in real time.
│
├── export_data.py           # Data export to CSV via pandas.
│
├── adm_manage.py            # Admin panel exclusive functions.
│                              Database CRUD operations via terminal.
│
├── database/
│   └── database.db          # SQLite database — tables: User, CalcInfos
│
├── csv_exported/
│   ├── User_data.csv
│   └── Calc_datas.csv
│
└── json_files/
    ├── userinfos.json
    └── calcinfos.json
```

### Main Data Flow

```
User types input
       ↓
main.py → user.WelcomeUser()
       ↓
   [new?] → INSERT INTO User (SQLite)
       ↓
Menu loop (match/case)
       ↓
┌──────────────────────────────────────┐
│ 1 → calculate_file → SQLite          │
│ 2 → user.show_user_data              │
│ 3 → database.get_calculator_history  │
│ 4 → get_exchange_rate → HTTP API     │
│ 5 → math_challenge_update            │
│ 6 → export_data → CSV                │
│ 7 → exit + connection.commit()       │
└──────────────────────────────────────┘
```

---

## Tech Stack

| Technology | Usage |
|---|---|
| **Python 3.10+** | Core language. Uses `match/case` (3.10+). |
| **SQLite3** | Persistence for users and operation history. |
| **requests** | HTTP calls to the live currency exchange API. |
| **pandas** | DataFrame creation and CSV export. |
| **uuid** | Unique ID generation for user records. |
| **datetime** | Access timestamp capture and formatting with `strftime`. |
| **time.perf_counter()** | High-precision timer for math challenges. |
| **math.sqrt()** | Primality check in the challenge module. |
| **random** | Random number and operator generation in challenges. |

---

## Key Technical Decisions

### Lambda dictionary instead of if/elif

```python
# Instead of:
if op == "+": return a + b
elif op == "-": return a - b
# ...

# We use:
operations_available = {"+": lambda a, b: ..., "-": lambda a, b: ...}
result = operations_available[op](num1, num2)
```

Benefits: shorter code, easy to add new operations, O(1) dictionary lookup instead of sequential condition checking.

### match/case instead of if/elif for the menu

`match/case` (Python 3.10+) is more readable for multiple branches over the same value, resembles a traditional switch/case, and makes future option additions cleaner without growing an `elif` chain.

### perf_counter() for the timer

`time.perf_counter()` uses the operating system's high-resolution clock, better suited for measuring short intervals than `time.time()`, which has lower precision depending on the OS.

### Loading usernames into memory at startup

In `user.py`, names are loaded from the database into a list when the module is first imported. This avoids a database query on every username attempt, making availability validation instant.

### DifficultyRange class

Centralizes all numeric ranges for each difficulty level in one place. Without it, values would be scattered as loose constants or hardcoded inside functions, making future adjustments harder to manage.

---

## How to Run

### Prerequisites

- Python 3.10 or higher
- pip

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run

```bash
python main.py
```

On the first run, the database is created automatically by `database.begginer_settings()`.

---

## Usage Examples

### New user registration and calculation

```
Do you already use JVBCalculator(Y/N)? N
Which username do you wanna be called? john
How old are you, john? 22
Do you already make birthday this year?(Y/N) Y

Welcome, john, born in 2002, you receive an access to the JVBCalculator

 MENU:
 1:Calculator
 2:My Informations
 3:Calculator History
 4:Currency converter
 5:Mental Math Challenge
 6:Export data
 7:Exit

Choose one of them options(1/2/3/4/5/6/7): 1
Which operation do you wanna make (+ - * / **)? **
Type the first number: 5
Type the second number: 3
Result: 5 ** 3 = 125
```

### Mental Math Challenge

```
Choose one of them options(1/2/3/4/5/6/7): 5

Welcome to the Mental Math Challenge! Here you will practice your
mental math skills by answering with integers only.

1 - Simple operations (with only two numbers)
2 - Complex operations (with more than two numbers)

Choose one operation among them(1/2): 2

1 - Easy  2 - Medium  3 - Hard  4 - Very Hard

Choose one level difficult among them(1/2/3/4): 3
(64 * 3) / (48 / 4) = 16
Perfect, you answered correctly in 12 seconds, congratulations!
```

### Currency Conversion

```
Choose one of them options(1/2/3/4/5/6/7): 4
Choose the coin you want to convert to BRL(USD/EUR/BTC): USD
How many USD do you wanna buy? 100
You will need R$515.00 to buy 100 USD
```

---

## What This Project Demonstrates

### Python Fundamentals
- Functions, scopes, dictionaries, lists, lambdas, and list comprehensions
- Exception handling with `try/except`, `ValueError`, and `ZeroDivisionError`
- Control flow including Python 3.10+ `match/case`
- Robust input validation with `while`, `try/except`, `.strip()`, `.upper()`
- String manipulation with f-strings and slicing
- Safe type conversions using `int`, `float`, and `round`

### Object-Oriented Programming
- `DifficultyRange` class with attributes and multiple access methods
- Encapsulation of related configuration in a single entity

### Data Persistence & Storage
- SQLite database creation and management with `sqlite3`
- INSERT and SELECT operations with filters
- Connection and transaction commit management
- JSON-based storage for user and operation logs

### External API Consumption
- Real-time data fetching with `requests`
- JSON response parsing
- Dynamic URL construction with runtime parameters

### Data Handling
- DataFrame creation and CSV export with `pandas`
- File existence check and removal with `os.path.isfile()` and `os.remove()`

### Modular Design & Architecture
- Separation of concerns across 8 distinct files
- Dictionary-based menus to eliminate long conditional chains
- Single-responsibility, well-named functions
- Scalable structure designed for future feature additions

### Algorithms & Logic
- Primality verification via square root
- Constrained random generation (non-prime numbers, guaranteed integer results)
- High-precision timing with `time.perf_counter()`
- Birth year calculation accounting for whether the birthday has occurred this year

---

## 🔮 Upcoming Features

- 🛠️ **Admin Panel** — complete CRUD: update and delete records from the database
- 📊 Improved data visualization
- 🔐 Better validation and security layers
