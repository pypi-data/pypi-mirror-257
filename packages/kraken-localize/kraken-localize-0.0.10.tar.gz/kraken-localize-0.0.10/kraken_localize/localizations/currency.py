
import copy
from kraken_localize.helpers import json
from kraken_localize.helpers import things
import functools

from babel.numbers import format_currency



def get_currency(code, currency=None, locale='en_US', digits=None):

    if isinstance(code, dict):
        value = code.get('price', None)
        currency = code.get('priceCurrency', None)

    else:
        value = code
    
    if not currency:
        currency = 'USD'

    return _get_currency(value, currency, locale, digits)
    

@functools.lru_cache(maxsize=128)
def _get_currency(value, currency=None, locale='en_US', digits=None):

    result = format_currency(value, currency, locale=locale, currency_digits=digits)
    return result



