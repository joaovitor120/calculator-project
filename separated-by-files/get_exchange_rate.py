import requests
coins_available = ["USD", "EUR", "BTC"]

def get_input_coin(): #get only the coin type the user want to convert
    coin_code = input("Choose the coin you want to convert to BRL(USD/EUR/BTC)").upper().strip() 
    while coin_code not in coins_available:
        print("Coin type isn't a valid option, please choose one valid among USD,EUR,BTC")
        coin_code = input("Choose the coin you want to convert to BRL(USD/EUR/BTC)").upper().strip()
    try:
        coin_quantity = float(input(f"How many {coin_code} do you wanna buy?"))
    except ValueError:
        print("Use a numerical value")
        coin_quantity = float(input(f"How many {coin_code} do you wanna buy?"))
    return coin_code, coin_quantity

def convertion_coin(rate, quantity): #to convert how many R$ you need to buy one {coin_code}
    moneyToBuy = quantity * rate
    return moneyToBuy

def proccess_main():
    coin_code, coin_quantity = get_input_coin()
    codein = "BRL"
    url = "https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL"
    request = requests.get(url)
    exchange_rate = request.json()[f"{coin_code}{codein}"]['bid']
    exchange_rate_float = round(float(exchange_rate), 2)

    moneyToBuy = round((convertion_coin(exchange_rate_float, coin_quantity)),2)
    print(f'You will need R${moneyToBuy} to buy {int(coin_quantity)} {coin_code}')


#200 OK