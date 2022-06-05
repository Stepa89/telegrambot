import requests
import json
from config import keys


class ConvertionException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def convert(guote: str, base: str, amount: str):
        if guote == base:
            raise ConvertionException(f'Невозможно перевести одинаковые валюты {base}.')

        try:
            guote_ticker = keys[guote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {guote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={guote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]] * amount

        return total_base
