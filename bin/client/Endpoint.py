class Endpoint:

    def __init__(self, path: str, signed: bool):
        self.__path = path
        self.__signed = signed

    def get_path(self):
        return self.__path

    def is_signed(self):
        return self.__signed