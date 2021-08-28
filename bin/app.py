import logging, os
from dotenv import load_dotenv

from client.exchange.BinanceClient import BinanceClient

# FOR TESTING PURPOSES ONLY!
# In production, the environment variables will be saved on os level
load_dotenv()

logging.basicConfig(format='[%(levelname)s]: %(message)s', level=logging.INFO)

def Main():
    client = BinanceClient(os.environ["API_KEY"], os.environ["API_SECRET"])
    print(client.get_system_status())

if __name__ == "__main__":
    Main()