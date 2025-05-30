import requests

API_KEY = "B2WRRMC5X88J85CGKDYSW8XSVJ4J2W4XX6"
WALLET_ADDRESS = "0x96FeF57e0dB8fEB445Af555a9A4768e1dB142946"
ETHERSCAN_API_URL = "https://api.etherscan.io/api"

def get_wallet_balance(address, api_key):
    params = {
        "module": "account",
        "action": "balance",
        "address": address,
        "tag": "latest",
        "apikey": api_key
    }
    try:
        response = requests.get(ETHERSCAN_API_URL, params=params)
        data = response.json()
        if data["status"] == "1":
            balance_wei = int(data["result"])
            balance_eth = balance_wei / 10**18
            return balance_eth
        else:
            return f"Помилка: {data['message']}"
    except Exception as e:
        return f"Помилка запиту: {str(e)}"

def get_wallet_transactions(address, api_key):
    params = {
        "module": "account",
        "action": "txlist",
        "address": address,
        "startblock": 0,
        "endblock": 99999999,
        "page": 1,
        "offset": 5,
        "sort": "desc",
        "apikey": api_key
    }
    try:
        response = requests.get(ETHERSCAN_API_URL, params=params)
        data = response.json()
        if data["status"] == "1":
            return data["result"]
        else:
            return f"Помилка: {data['message']}"
    except Exception as e:
        return f"Помилка запиту: {str(e)}"

def main():
    balance = get_wallet_balance(WALLET_ADDRESS, API_KEY)
    print(f"Баланс: {balance} ETH" if isinstance(balance, float) else balance)
    
    transactions = get_wallet_transactions(WALLET_ADDRESS, API_KEY)
    if isinstance(transactions, list):
        for tx in transactions:
            print(f"Від: {tx['from'][:10]}...")
            print(f"До: {tx['to'][:10]}...")
            value_eth = int(tx['value']) / 10**18
            print(f"Сума: {value_eth} ETH")
            print(f"Дата: {tx['timeStamp']}")
    else:
        print(transactions)

if __name__ == "__main__":
    main()
    
