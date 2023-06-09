import json
import time
from colorama import Fore, Style


# Returns string formatted timestamp
def get_timestamp() -> str:
    return time.strftime(f'{Style.BRIGHT + Fore.LIGHTBLUE_EX}%H:%M:%S EST{Style.RESET_ALL} ', time.localtime())


# Retrieves value from cfg.json
def get_value(key: str) -> str:
    with open('cfg.json', 'r') as f:
        token = json.load(f)[key]
        f.close()
        return token
