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

        with open('alerts.json', 'r') as f:
            self.alerts = json.load(f)


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

        selloutPrice = self.account['selloutPrice']

        # calculate the current worth in dollars of bitcoin quantity
        worth = price * quantityBought
        self.account['gain'] = worth - purchasePrice

        # writes new account high
        if worth > highestWorth:

            self.account['highestWorth'] = worth
            self.account['selloutPrice'] = ((highestWorth - purchasePrice) * 0.92 + purchasePrice)

            with open('account.json', 'w') as f:
                account = json.dump(self.account, f)

        # sends alert if the price drops below the thresh-hold that was set
        if worth < selloutPrice:
            string = self.alerts['priceDrop']
            self.sendPriceAlert(self.number, self.formatMessage(string))
            exit()

        # the difference between the present worth and the purchase price
        difference = worth - purchasePrice

        # print the gain / loss of the purhcase
        if difference > 0:
            str = '{}\tMONEY GAINED:\t$ {}\tWORTH: $ {}'.format(datetime.datetime.now(), difference, worth)

        if difference < 0:
            str = 'MONEY LOST:\t$ {}'.format(datetime.datetime.now(), difference)

        # if a string is crafted then write it to the report
        if str != None:
            with open('report.txt', 'a') as f:
                f.write(str + '\n')

    # send alert about the price
    def sendPriceAlert(self, number, message):
        client = Client(self.sid, self.token)
        message = client.messages.create(
            to=number,
            from_="+19389999671",
            body=message)

    def formatMessage(self, string):
        string = '~\\\\~ ' + string + ' ~//~'
        return string

if __name__ == '__main__':

    drew = Drew()

    while True:
        try:
            drew.compare(drew.fetch())
            time.sleep(15)
        except:
            pass
