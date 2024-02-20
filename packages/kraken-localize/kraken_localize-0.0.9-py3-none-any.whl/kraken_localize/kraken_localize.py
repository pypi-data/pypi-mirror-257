
    
from kraken_localize.helpers import json
from kraken_localize.helpers import things

import datetime

from kraken_localize import localizations

"""
Notes:
To access files in data directory, use:
new_path = pkg_resources.resource_filename('kraken_localize', old_path)


"""
records = []

def _c(code, currency=None, language='en_US', digits=None):
    """Currency
    """
    return localizations.currency._get_currency(code, currency, language, digits)
    
def _n(code, language='en_US', digits=None, unitCode=None):
    """Number
    """
    return localizations.number._get_number(code, language, digits, unitCode)

def _ncode(code, language='en_US', digits=None, unitCode=None):
    """Number
    """
    return localizations.number._get_unitCode(code, language, digits, unitCode)

def _d(code, language='en_US', timezone=None):
    """Date
    """
    return localizations.date._get_date(code, language, timezone)

def _delta(code, language="en_US", to=None, timezone=None):
    """Date delta from today
    """
    return localizations.date._get_delta(code, language, to, timezone)









def _l2(code, number='s', language='en_US', digits=None):
    """Return localization
    number: ['s', 'p']    singular or plural
    
    """

    if isinstance(code, dict):
        record_type = code.get('@type', None)
        if record_type == 'quantitativeValue': 
            return localizations.number._get_number(code, language, digits)
        elif record_type == "priceSpecification":
            localizations.currency._get_currency(code, None, language, digits)
            
        else:
            return code
    
    elif isinstance(code, (datetime.date, datetime.datetime)):
        return localizations.date._get_date(code, language)

    elif isinstance(code, (int, float)):
        return localizations.number._get_number(code, language, digits)
        
    else:
        return localizations.text._get_term(code, number, language)


def new_entry(id, language, value_singular, value_plural):
    return localizations.text.new_entry(id, language, value_singular, value_plural)

def _z(code, **kwargs):
    print(kwargs)