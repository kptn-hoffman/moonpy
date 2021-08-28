import logging

from client.Client import Client

class BinanceClient(Client):
    def __init__(self) -> None:
        super().__init__()
        logging.info("BinanceClient successfully initialized")