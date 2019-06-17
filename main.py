import requests
from bs4 import BeautifulSoup
import json

def fetch():
    # get the
    r = requests.get('https://api.coinmarketcap.com/v1/ticker/bitcoin/')
    r = r.json()[0]
    with open('h.json', 'w') as f:
        json.dump(r, f)
    return r

def compare(r):
    # the current price of bitcoin
    price = float(r['price_usd'])
    with open('account.json') as f:
        account = json.load(f)

    quantity = account['quantity']
    worth = price * quantity
    difference = worth - account['worth']
    if difference > 0:
        print('GAIN:\t{}'.format(difference))
    if difference < 0:
        print('LOSS:\t{}'.format(difference))

if __name__ == '__main__':
    compare(fetch())
