import requests
from log import logger 
from constants import Constants
from datetime import datetime
if __name__ == '__main__':
    logger.info('main start')
    url = Constants.AMBERDATA_BASE_MARKET + '/ohlcv/information?exchange=binance,huobi'
    headers = { 'x-api-key': Constants.AMBERDATA_API_KEY }
    response = requests.get(url, headers=headers)
    payload = response.json()['payload']
    for exchange in ['binance', 'huobi']:
        logger.info('{} eth_btc startDate is {}'.format(exchange, datetime.utcfromtimestamp(payload[exchange]['eth_btc']['startDate']/1000.0).isoformat()))
    logger.info('main end')