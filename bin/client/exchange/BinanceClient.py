import logging, hmac, hashlib
from datetime import datetime

from client.Client import Client

class BinanceClient(Client):

    API_BASE_URL = 'https://api.binance.com'
    API_MIRROR_URLS = [
        'https://api1.binance.com',
        'https://api2.binance.com',
        'https://api3.binance.com'
    ]

    def __init__(self, api_key: str, api_secret: str) -> None:
        super().__init__()
        self.API_SECRET = api_secret
        self.API_KEY = api_key
        logging.info("BinanceClient successfully initialized")

    def get_timestamp(self):
        now = datetime.now()
        timestamp = int(datetime.timestamp(now)*1000)
        return timestamp

    def get_signature(self, query_string: str):
        return hmac.new(
            self.API_SECRET.encode('utf-8'),
            query_string.strip("?").encode('utf-8'),
            hashlib.sha256).hexdigest()
        