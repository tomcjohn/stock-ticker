from googlefinance import getQuotes
import json
import requests


print('Loading function')


# curl -s "http://finance.google.com/finance/info?client=ig&q=FRA:CXH"


def get_stock_quote(stock_symbol):
    response = getQuotes('FRA:CXH')
    print json.dumps(getQuotes('FRA:CXH'), indent=2)
    quote = response[0]['LastTradePrice']
    return quote


def lambda_handler(event, context):
    stock_quote_eur = get_stock_quote('FRA:CXH')
    print('Quote (EUR): ' + stock_quote_eur)
    return


if __name__ == '__main__':
    lambda_handler(None, None)

