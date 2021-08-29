from errors.Exceptions import MissingMandatoryParamError
import logging, hmac, hashlib, requests

from urllib.parse import urlencode
from datetime import datetime

from client.Client import Client
from client.Endpoint import Endpoint

class BinanceClient(Client):

    API_BASE_URL = 'https://api.binance.com'
    API_MIRROR_URLS = [
        'https://api1.binance.com',
        'https://api2.binance.com',
        'https://api3.binance.com'
    ]

    # Wallet endpoints
    SYSTEM_STATUS_ENDPOINT  = Endpoint('sapi/v1/system/status', signed=False, mandatory_params=())
    ALL_COINS_INFO_ENDPOINT = Endpoint('sapi/v1/capital/config/getall', signed=True, mandatory_params=())
    DAILY_SNAPSHOT_ENDPOINT = Endpoint('sapi/v1/accountSnapshot', signed=True, mandatory_params=('type',))

    # Market data endpoints
    EXCHANGE_INFO_ENDPOINT    = Endpoint('api/v3/exchangeInfo', signed=False, mandatory_params=())
    CANDLESTICK_DATA_ENDPOINT = Endpoint('api/v3/klines', signed=False, mandatory_params=('symbol', 'interval'))

    # Spot trade endpoints
    TEST_NEW_ORDER_ENDPOINT = Endpoint('api/v3/order/test', signed=True, mandatory_params=('symbol', 'side', 'type', 'quantity'))
    NEW_ORDER_ENDPOINT      = Endpoint('api/v3/order', signed=True, mandatory_params=('symbol', 'side', 'type', 'quantity'))

    URL_TEMPLATE = "{}/{}{}"

    def __init__(self, api_key: str, api_secret: str) -> None:
        super().__init__()
        self.__API_KEY = api_key
        self.__API_SECRET = api_secret
        logging.info('BinanceClient successfully initialized')

    def get_system_status(self):
        system_status_url = self.__new_request_url(self.SYSTEM_STATUS_ENDPOINT, {})
        logging.info('Getting system status')
        return requests.get(url=system_status_url, headers=self.__get_default_headers()).json()
    
    def get_all_coins_info(self):
        all_coins_info_url = self.__new_request_url(self.ALL_COINS_INFO_ENDPOINT, {})
        logging.info('Getting all coins info')
        return requests.get(url=all_coins_info_url, headers=self.__get_default_headers()).json()

    def get_daily_account_snapshot(self, params: dict):
        self.DAILY_SNAPSHOT_ENDPOINT.check_mandatory_params(params)
        daily_snapshot_url = self.__new_request_url(self.DAILY_SNAPSHOT_ENDPOINT, params)
        logging.info('Getting daily account snapshot')
        return requests.get(url=daily_snapshot_url, headers=self.__get_default_headers()).json()
    
    def get_most_recent_account_snapshot(self, params: dict):
        logging.info('Getting most recent account snapshot')
        return self.get_daily_account_snapshot(params)['snapshotVos'][0]['data']['balances']

    def get_asset_info(self, params, asset: str):
        logging.info('Getting info on {}'.format(asset))
        for assetDict in self.get_most_recent_account_snapshot(params):
            if assetDict['asset'] == asset:
                return assetDict
        return {}

    def get_exchange_info(self, params: dict = {}):
        logging.info('Getting exchange info')
        exchange_info_url = self.__new_request_url(self.EXCHANGE_INFO_ENDPOINT, params)
        return requests.get(url=exchange_info_url, headers=self.__get_default_headers()).json()

    def get_candlestick_data(self, params: dict):
        logging.info('Getting candlestick data')
        candlestick_data_url = self.__new_request_url(self.CANDLESTICK_DATA_ENDPOINT, params)
        return requests.get(url=candlestick_data_url, headers=self.__get_default_headers()).json()

    def test_new_order(self, params: dict):
        test_new_order_url = self.__new_request_url(self.TEST_NEW_ORDER_ENDPOINT, params)
        return requests.post(url=test_new_order_url, headers=self.__get_default_headers()).json()

    def __new_request_url(self, endpoint: Endpoint, params: dict) -> str:
        try:
            endpoint.check_mandatory_params(params)
            if endpoint.is_signed():
                params['timestamp'] = self.__get_timestamp()
                params['signature'] = self.__get_signature(urlencode(params))
            query_string = self.__get_query_string(params)
            return self.URL_TEMPLATE.format(self.API_BASE_URL, endpoint.get_path(), query_string)
        except MissingMandatoryParamError as err:
            # TODO: stop bot!
            err.with_traceback()

    def __get_query_string(self, params: dict):
        if params:
            return "?" + urlencode(params)
        return ""

    def __get_default_headers(self) -> dict:
        headers = {
            'Accept': 'application/json',
            'X-MBX-APIKEY': self.__API_KEY
        }
        return headers

    # TODO: consider moving to Client class
    def __get_timestamp(self) -> int:
        now = datetime.now()
        timestamp = int(datetime.timestamp(now)*1000)
        return timestamp

    def __get_signature(self, query_string: str):
        return hmac.new(
            self.__API_SECRET.encode('utf-8'),
            query_string.strip("?").encode('utf-8'),
            hashlib.sha256).hexdigest()
        