import requests
import statistics
from log import logger 
from urllib.parse import urlencode
from constants import Constants
def join(data_a, data_b, key_index, value_index):
    data_b_dict = { x[key_index]: x[value_index] for x in data_b }
    data_joined = []
    for x in data_a:
        if x[key_index] in data_b_dict:
            data_joined.append([x[key_index], x[value_index], data_b_dict[x[key_index]]])
    return data_joined
            
if __name__ == '__main__':
    logger.info('main start')
    url = Constants.AMBERDATA_BASE_MARKET + '/ohlcv/eth_btc/historical?'
    filters = {}
    filters['exchange'] = 'binance,huobi'
    filters['timeInterval'] = 'minutes'
    filters['startDate'] = 1556064000 #'2019-04-24'
    filters['endDate'] = 1558656000 #'2019-05-24'
    url += urlencode(filters)
    logger.info('url = {}'.format(url))
    headers = { 'x-api-key': Constants.AMBERDATA_API_KEY }
    response = requests.get(url, headers=headers, timeout=600)
    data = response.json()['payload']['data']
    data_joined = join(data['binance'], data['huobi'], 0, 4)
    diff_price_stdev = statistics.stdev([x[1] - x[2] for x in data_joined])
    logger.info('diff_price_stdev = {}'.format(diff_price_stdev))
    logger.info('main end')