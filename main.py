import requests
from bs4 import BeautifulSoup
import json
import time

def fetch():
    # get the
    r = requests.get('https://api.coinmarketcap.com/v1/ticker/bitcoin/')
    r = r.json()[0]
    with open('h.json', 'w') as f:
        json.dump(r, f)
    return r

def compare(r):

    # load our account detail
    with open('account.json') as f:
        account = json.load(f)

    # the current price of bitcoin
    price = float(r['price_usd'])

    # the amount bought and the price it was purchased for
    quantityBought = account['quantityBought']
    purchasePrice = account['purchasePrice']

    # calculate the current worth of bitcoin quantity
    worth = price * quantityBought
    difference = worth - purchasePrice

    # print the gain / loss of the purhcase
    if difference > 0:
        print('MONEY GAINED:\t$ {}'.format(difference))
    if difference < 0:
        print('MONEY LOST:\t$ {}'.format(difference))

if __name__ == '__main__':
    while True:
        compare(fetch())
        time.sleep(15)
