import logging, math

from client.exchange.BinanceClient import BinanceClient

logging.basicConfig(format='[%(levelname)s]: %(message)s', level=logging.INFO)

client = BinanceClient("asdasd", "asasde")

print(client.sign_request("asd?Asda?asd"))