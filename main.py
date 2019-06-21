import requests
from bs4 import BeautifulSoup
import json
import time
import datetime
from twilio.rest import Client

class Drew():
    def __init__(self):

        with open('account.json', 'r') as f:
            self.account = json.load(f)

        self.sid = self.account['accountSID']
        self.token = self.account['authToken']
        self.number = self.account['phoneNumber']

    def fetch(self):
        # get the
        r = requests.get('https://api.coinmarketcap.com/v1/ticker/bitcoin/')
        r = r.json()[0]

        with open('h.json', 'w') as f:
            json.dump(r, f)
        return r


    def compare(self, r):

        # the current price of bitcoin
        price = float(r['price_usd'])

        # the amount bought and the price it was purchased for
        quantityBought = self.account['quantityBought']
        purchasePrice = self.account['purchasePrice']
        highestWorth = self.account['highestWorth']

        selloutPrice = self.account['highestWorth'] * .985

        # calculate the current worth in dollars of bitcoin quantity
        worth = price * quantityBought

        # writes new account high
        if worth > highestWorth:

            self.account['highestWorth'] = worth
            self.account['selloutPrice'] = ((highestWorth - purchasePrice) * 0.92 + purchasePrice)


            with open('account.json', 'w') as f:
                account = json.dump(self.account, f)

        # sends alert if the price drops below the thresh-hold that was set
        if worth < selloutPrice:
            self.sendPriceAlert(self.number, '~\\\\~ CHECK BITCOIN WALLET ~//~')
            exit()
        difference = worth - purchasePrice

        # print the gain / loss of the purhcase
        if difference > 0:
            str = '{}\tMONEY GAINED:\t$ {}\tWORTH: $ {}'.format(datetime.datetime.now(), difference, worth)
            print(str)
        if difference < 0:
            str = 'MONEY LOST:\t$ {}'.format(datetime.datetime.now(), difference)
            print(str)

        if str != None:
            with open('report.txt', 'a') as f:
                f.write(str + '\n')

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
