import io
from googlefinance import getQuotes
import json
from lxml import etree
import requests


# http://finance.google.com/finance/info?client=ig&q=FRA:CXH
# https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml


print('Loading function')


NUM_STOCKS = 3500.0


def get_stock_quote(stock_symbol):
    response = getQuotes('FRA:CXH')
    return response[0]['LastTradePrice']


def get_exchange_rate(currency):
    response = requests.get('https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml')
    response_xml = response.text
    response_xml = response_xml.replace('<?xml version="1.0" encoding="UTF-8"?>', '<?xml version="1.0"?>')
    response_xml = response_xml.replace('<gesmes:Envelope xmlns:gesmes="http://www.gesmes.org/xml/2002-08-01" xmlns="http://www.ecb.int/vocabulary/2002-08-01/eurofxref">', '<Envelope>')
    response_xml = response_xml.replace('gesmes:', '')
    tree = etree.fromstring(response_xml)
    xpath_expr = '//Cube[@currency="AUD"]'
    nodes = tree.xpath(xpath_expr, namespaces={'gesmes': 'http://www.gesmes.org/xml/2002-08-01'})
    return nodes[0].get("rate")


def lambda_handler(event, context):
    stock_quote_eur = float(get_stock_quote('FRA:CXH'))
    print('Quote (EUR): ' + str(stock_quote_eur))
    rate_eur_to_aud = float(get_exchange_rate('AUD'))
    print('Rate (EUR->AUD): ' + str(rate_eur_to_aud))
    stock_value_aud = stock_quote_eur * rate_eur_to_aud
    print('Stock value (AUD): ' + str(stock_value_aud))
    total_stock_value_aud = NUM_STOCKS * stock_value_aud
    print('Total stock value (AUD): ' + str(total_stock_value_aud))
    return total_stock_value_aud


if __name__ == '__main__':
    lambda_handler(None, None)

