import logging, hmac, hashlib
from urllib.parse import urlencode
from datetime import datetime

from client.Client import Client

class BinanceClient(Client):

    API_BASE_URL = 'https://api.binance.com'
    API_MIRROR_URLS = [
        'https://api1.binance.com',
        'https://api2.binance.com',
        'https://api3.binance.com'
    ]

    URL_TEMPLATE = "{}/{}?{}"

    def __init__(self, api_key: str, api_secret: str) -> None:
        super().__init__()
        self.API_KEY = api_key
        self.API_SECRET = api_secret
        logging.info('BinanceClient successfully initialized')

    def _new_request_url(self, path: str, params: dict, signed: bool = False) -> str:
        if signed:
            params["timestamp"] = self._get_timestamp()
            params["signature"] = self._get_signature(urlencode(params))
        query_string = urlencode(params)
        return self.URL_TEMPLATE.format(self.API_BASE_URL, path, query_string)

    def _get_default_headers(self) -> dict:
        headers = {
            'Accept': 'application/json',
            'X-MBX-APIKEY': self.API_KEY
        }
        return headers

    # TODO: consider moving to Client class
    def _get_timestamp(self) -> int:
        now = datetime.now()
        timestamp = int(datetime.timestamp(now)*1000)
        return timestamp

    def _get_signature(self, query_string: str):
        return hmac.new(
            self.API_SECRET.encode('utf-8'),
            query_string.strip("?").encode('utf-8'),
            hashlib.sha256).hexdigest()
        