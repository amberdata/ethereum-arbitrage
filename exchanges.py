import requests
from log import logger 
from constants import Constants
if __name__ == '__main__':
    logger.info('main start')
    url = Constants.AMBERDATA_BASE_MARKET + '/exchanges'
    headers = { 'x-api-key': Constants.AMBERDATA_API_KEY }
    response = requests.get(url, headers=headers)
    payload = response.json()['payload']
    exchange_count_pair = [(k, len(v)) for (k,v) in payload.items()]
    exchange_count_pair.sort(key=lambda x: x[1], reverse=True)
    logger.info(exchange_count_pair[:10])
    pair_count_exchange_dict = {}
    for k, v in payload.items():
        for pair in list(v.keys()):
            if pair not in pair_count_exchange_dict:
                pair_count_exchange_dict[pair] = 0
            pair_count_exchange_dict[pair] += 1
    pair_count_exchange = [(k, v) for (k,v) in pair_count_exchange_dict.items()]
    pair_count_exchange.sort(key=lambda x: x[1], reverse=True)
    logger.info(pair_count_exchange[:10])
    logger.info('main end')