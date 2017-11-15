from datetime import date, datetime, timedelta
import json
from lxml import etree
from requests import get, post


# https://www.alphavantage.co/query?apikey=H5TOEVP1UDZQ26SV&outputsize=compact&datatype=json&function=TIME_SERIES_DAILY&symbol=CXENSE.OL
# https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml


print('Loading function')

AUD = 'AUD'
NOK = 'NOK'

AV_APIKEY = 'H5TOEVP1UDZQ26SV'
STOCK_SYMBOL = 'CXENSE.OL'
ALPHAVANTAGE_URL = 'https://www.alphavantage.co/query?datatype=json&outputsize=compact&function=TIME_SERIES_DAILY&apikey=' + AV_APIKEY + '&symbol=' + STOCK_SYMBOL
ECB_URL = 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml'
ES_ENDPOINT_URL = 'https://search-stock-ticker-hihtqyk272pvyvup7j2gfatg4y.ap-southeast-2.es.amazonaws.com/stock-ticker/stock-value'
NUM_STOCKS = 3500.0


def get_stock_quote():
    print 'Retrieving stock quote: ' + ALPHAVANTAGE_URL
    r = get(ALPHAVANTAGE_URL)
    json_str = r.text
    parsed_json = json.loads(json_str)
    # most recent stock value available from AlphaVantage is yesterday's
    yesterday = date.today() - timedelta(1)
    return parsed_json['Time Series (Daily)'][str(yesterday)]['4. close']


def download_exchange_rates():
    print 'Retrieving exchange rate: ' + ECB_URL
    r = get(ECB_URL)
    xml = r.text
    xml = xml.replace('<?xml version="1.0" encoding="UTF-8"?>', '<?xml version="1.0"?>')
    xml = xml.replace('<gesmes:Envelope xmlns:gesmes="http://www.gesmes.org/xml/2002-08-01" xmlns="http://www.ecb.int/vocabulary/2002-08-01/eurofxref">', '<Envelope>')
    xml = xml.replace('gesmes:', '')
    return xml


def get_exchange_rate(exchange_rates_xml, currency_code):
    tree = etree.fromstring(exchange_rates_xml)
    xpath_expr = '//Cube[@currency="' + currency_code + '"]'
    nodes = tree.xpath(xpath_expr, namespaces={'gesmes': 'http://www.gesmes.org/xml/2002-08-01'})
    return nodes[0].get("rate")


def send_to_elasticsearch(update_date, value, currency_code):
    data_struct = '{ "update_date": "' + str(update_date) + '" ,"value": "' + str(value) + '" ,"currency": "' + str(currency_code) + '" }'
    r = post(ES_ENDPOINT_URL, data = data_struct)
    r.raise_for_status()
    print("Elasticsearch response: " + str(r.status_code))
    return


def lambda_handler(event, context):
    now = datetime.utcnow().isoformat()

    stock_quote_nok = float(get_stock_quote())
    print('Quote (NOK): ' + str(stock_quote_nok))

    exchange_rates_xml = download_exchange_rates()

    rate_nok_to_eur = 1 / float(get_exchange_rate(exchange_rates_xml, NOK))
    print('Rate (NOK->EUR): ' + str(rate_nok_to_eur))

    rate_eur_to_aud = float(get_exchange_rate(exchange_rates_xml, AUD))
    print('Rate (EUR->AUD): ' + str(rate_eur_to_aud))

    rate_nok_to_aud = rate_nok_to_eur * rate_eur_to_aud
    print('Rate (NOK->AUD): ' + str(rate_nok_to_aud))

    stock_value_aud = stock_quote_nok * rate_nok_to_aud
    print('Stock value (AUD): ' + str(stock_value_aud))

    total_stock_value_aud = NUM_STOCKS * stock_value_aud
    print('Total stock value (AUD): ' + str(total_stock_value_aud))

    send_to_elasticsearch(now, total_stock_value_aud, AUD)

    return total_stock_value_aud


if __name__ == '__main__':
    lambda_handler(None, None)
