from errors.Exceptions import MissingMandatoryParamError

class Endpoint:

    def __init__(self, path: str, signed: bool, mandatory_params: tuple):
        self.__path = path
        self.__signed = signed
        self.__mandatory_params = mandatory_params

    def get_path(self) -> str:
        return self.__path

    def is_signed(self) -> bool:
        return self.__signed

    def get_mandatory_params(self) -> tuple:
        return self.__mandatory_params
    
    def check_mandatory_params(self, params: dict) -> bool:
        for mandatory_param in self.__mandatory_params:
            if not mandatory_param in params:
                raise MissingMandatoryParamError(mandatory_param)
        return True