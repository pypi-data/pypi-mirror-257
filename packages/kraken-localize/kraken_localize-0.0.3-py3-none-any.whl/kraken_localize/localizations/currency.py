
import copy
from kraken_localize.helpers import json
from kraken_localize.helpers import things


from babel.numbers import format_currency



def _get_currency(code, currency=None, language='en_US', digits=None):

    if isinstance(code, dict):
        code = code.get('price', None)
        currency = code.get('priceCurrency', None)

    if not currency:
        currency = 'USD'

    result = format_currency(code, currency, locale=language, currency_digits=digits)
    return result






