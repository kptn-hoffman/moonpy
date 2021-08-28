from enums.constants import OrderType, OrderSide, WalletType

class Client:
    def __init__(self) -> None:
        pass

    def health_check(self):
        raise NotImplementedError

    def get_balance(self, wallet_type: WalletType):
        raise NotImplementedError
    
    def place_order(self, order_side: OrderSide,order_type: OrderType):
        raise NotImplementedError

    def cancel_order(self, order_id: int, symbol: str):
        raise NotImplementedError
    
    def cancel_all_orders(self, symbol: str):
        raise NotImplementedError

    def get_order_status(self, order_id: int, symbol: str):
        raise NotImplementedError
    
    def get_all_orders_staus(self, symbol: str = None):
        raise NotImplementedError

    def _get_timestamp(self):
        raise NotImplementedError

    def _get_signature(self, query_string):
        raise NotImplementedError

    