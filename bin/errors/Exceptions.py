import logging

class MissingMandatoryParamError(Exception):
    def __init__(self, param: str, message='Mandatory parameter "{}" missing from request') -> None:
        logging.error(message.format(param))
        super().__init__()