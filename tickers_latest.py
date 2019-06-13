import requests
from concurrent.futures import ThreadPoolExecutor,as_completed
from log import logger

import time
import json
from constants import Constants

sigma = 3.862523415579312e-05

def place_order_if_condition_met(prices):
    if prices['binance_bid'] and prices['huobi_ask']:
        diff = abs(prices['binance_bid'] - prices['huobi_ask'])
        if diff > 2 * sigma:
            logger.info('here we need to take some positions')
        elif diff < 0.1 * sigma:
            logger.info('here we need to exit some positions')
    if prices['binance_ask'] and prices['huobi_bid']:
        diff = abs(prices['binance_ask'] - prices['huobi_bid'])
        if diff > 2 * sigma:
            logger.info('here we need to take some positions')
        elif diff < 0.1 * sigma:
            logger.info('here we need to exit some positions')
    
if __name__ == '__main__':
    logger.info('main start')
    while True:
        url = Constants.AMBERDATA_BASE_MARKET + '/tickers/eth_btc/latest?exchange=binance,huobi'
        headers = { 'x-api-key': Constants.AMBERDATA_API_KEY }
        response = requests.get(url, headers=headers)
        payload = response.json()['payload']
        prices = {}
        prices['binance_bid'] = payload['binance'].get('bid')
        prices['binance_ask'] = payload['binance'].get('ask')
        prices['huobi_bid'] = payload['huobi'].get('bid')
        prices['huobi_ask'] = payload['huobi'].get('ask')
        place_order_if_condition_met(prices)
        time.sleep(60)
    logger.info('main end')
