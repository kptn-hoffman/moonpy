import logging, math

from client.exchange.BinanceClient import BinanceClient

logging.basicConfig(format='[%(levelname)s]: %(message)s', level=logging.INFO)

client = BinanceClient("asdasd", "asasde")

print(client._new_request_url("sapi/v1/accountSnapshot", {"asdasd": "wasdcxsz", "xczc": "asdxvv"}, True))