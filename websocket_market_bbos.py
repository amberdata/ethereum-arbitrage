import websocket
from log import logger
import ssl
import json
from constants import Constants

prices = {}
sigma = 3.862523415579312e-05
def on_open(ws):
    logger.info('websocket {} was connected'.format(ws.url))
    ws.send(json.dumps({
        'jsonrpc': '2.0',
        'id': 1,
        'method': 'subscribe',
        'params': ['market:bbos', {'pair': 'eth_btc', 'exchange': 'binance'}]
    }))
    ws.send(json.dumps({
        'jsonrpc': '2.0',
        'id': 2,
        'method': 'subscribe',
        'params': ['market:bbos', {'pair': 'eth_btc', 'exchange': 'huobi'}]
    }))

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

def on_message(ws, message):
    json_message = json.loads(message)
    if json_message.get('params') and json_message.get('params').get('result'):
        result = json_message.get('params').get('result')
        if result['exchange'] == 'binance':
            if result['isBid']:
                prices['binance_bid'] = result['price']
                place_order_if_condition_met(prices)
            else:
                prices['binance_ask'] = result['price']
                place_order_if_condition_met(prices)
        elif result['exchange'] == 'huobi':
            if result['isBid']:
                prices['huobi_bid'] = result['price']
                place_order_if_condition_met(prices)
            else:
                prices['huobi_ask'] = result['price']
                place_order_if_condition_met(prices)
if __name__ == '__main__':
    logger.info('main start')
    ws = websocket.WebSocketApp(Constants.AMBERDATA_WEBSOCKET_BASE)
    ws.header = {'x-api-key': Constants.AMBERDATA_API_KEY}
    ws.on_open = on_open
    ws.on_message = on_message
    ws.run_forever(sslopt={'cert_reqs': ssl.CERT_NONE})
    logger.info('main end')
