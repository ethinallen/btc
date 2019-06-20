import requests
from bs4 import BeautifulSoup
import json
import time
import datetime
from twilio.rest import Client

class Drew():
    def __init__(self):

        with open('account.json') as f:
            account = json.load(f)
        self.sid = account['accountSID']
        self.token = account['authToken']
        self.number = account['phoneNumber']

    def fetch(self):
        # get the
        r = requests.get('https://api.coinmarketcap.com/v1/ticker/bitcoin/')
        r = r.json()[0]
        with open('h.json', 'w') as f:
            json.dump(r, f)
        return r


    def compare(self, r):

        # load our account detail
        with open('account.json') as f:
            account = json.load(f)

        # the current price of bitcoin
        price = float(r['price_usd'])

        # the amount bought and the price it was purchased for
        quantityBought = account['quantityBought']
        purchasePrice = account['purchasePrice']
        highestWorth = account['highestWorth']

        selloutPrice = account['highestWorth'] * .95

        # calculate the current worth in dollars of bitcoin quantity
        worth = price * quantityBought

        if worth > highestWorth:
            account['highestWorth'] = worth
            with open('account.json', 'w') as f:
                account = json.dump(account, f)

        if worth < selloutPrice:
            self.sendPriceAlert(self.number, '~\\\\~ CHECK BITCOIN WALLET ~//~')
            exit()
        difference = worth - purchasePrice

        # print the gain / loss of the purhcase
        if difference > 0:
            print('{}\tMONEY GAINED:\t$ {}'.format(datetime.datetime.now(), difference))
        if difference < 0:
            print('MONEY LOST:\t$ {}'.format(datetime.datetime.now(), difference))

    def sendPriceAlert(self, number, message):
        client = Client(self.sid, self.token)
        message = client.messages.create(
            to=number,
            from_="+19389999671",
            body=message)

if __name__ == '__main__':

    drew = Drew()
    while True:
        drew.compare(drew.fetch())
        time.sleep(15)
