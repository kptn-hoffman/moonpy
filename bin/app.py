import logging

from client.exchange.BinanceClient import BinanceClient

logging.basicConfig(format='[%(levelname)s]: %(message)s', level=logging.INFO)

client = BinanceClient()