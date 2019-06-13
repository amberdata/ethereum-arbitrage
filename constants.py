import os
class Constants:
    AMBERDATA_API_KEY = os.environ['AMBERDATA_API_KEY']
    AMBERDATA_BASE = 'https://web3api.io/api/v1'
    AMBERDATA_BASE_MARKET = AMBERDATA_BASE + '/market'
    AMBERDATA_WEBSOCKET_BASE = 'wss://ws.web3api.io'

    