from datetime import datetime

from googlefinance import getQuotes
from lxml import etree
import requests


# http://finance.google.com/finance/info?client=ig&q=FRA:CXH
# https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml


print('Loading function')


NUM_STOCKS = 3500.0
ES_ENDPOINT_URL = 'https://search-stock-ticker-hihtqyk272pvyvup7j2gfatg4y.ap-southeast-2.es.amazonaws.com/stock-ticker/stock-value'


def get_stock_quote(stock_symbol):
    response = getQuotes('FRA:CXH')
    return response[0]['LastTradePrice']


def get_exchange_rate(currency_code):
    r = requests.get('https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml')
    xml = r.text
    xml = xml.replace('<?xml version="1.0" encoding="UTF-8"?>', '<?xml version="1.0"?>')
    xml = xml.replace('<gesmes:Envelope xmlns:gesmes="http://www.gesmes.org/xml/2002-08-01" xmlns="http://www.ecb.int/vocabulary/2002-08-01/eurofxref">', '<Envelope>')
    xml = xml.replace('gesmes:', '')
    tree = etree.fromstring(xml)
    xpath_expr = '//Cube[@currency="' + currency_code + '"]'
    nodes = tree.xpath(xpath_expr, namespaces={'gesmes': 'http://www.gesmes.org/xml/2002-08-01'})
    return nodes[0].get("rate")


def send_to_elasticsearch(update_date, value, currency_code):
    data_struct = {
        'update_date' : update_date,
        'value' : value,
        'currency': currency_code
    }
    print('data_struct:')
    print(data_struct)
    r = requests.post(ES_ENDPOINT_URL, data = data_struct)
    print r.status_code
    r.raise_for_status()
    return


def lambda_handler(event, context):
    currency_code = 'AUD'
    now = datetime.utcnow().isoformat()

    stock_quote_eur = float(get_stock_quote('FRA:CXH'))
    print('Quote (EUR): ' + str(stock_quote_eur))
    
    rate_eur_to_aud = float(get_exchange_rate(currency_code))
    print('Rate (EUR->' + currency_code + '): ' + str(rate_eur_to_aud))
    
    stock_value_aud = stock_quote_eur * rate_eur_to_aud
    print('Stock value (' + currency_code + '): ' + str(stock_value_aud))
    
    total_stock_value_aud = NUM_STOCKS * stock_value_aud
    print('Total stock value (' + currency_code + '): ' + str(total_stock_value_aud))
    
    send_to_elasticsearch(now, total_stock_value_aud, currency_code)
    
    return total_stock_value_aud


if __name__ == '__main__':
    lambda_handler(None, None)
