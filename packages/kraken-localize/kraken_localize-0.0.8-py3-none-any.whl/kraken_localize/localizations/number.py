
import copy
from kraken_localize.helpers import json
from kraken_localize.helpers import things
import os
from babel.numbers import format_decimal, format_currency, format_number, format_compact_decimal, format_percent

import datetime

from pint import UnitRegistry


def _get_number(code, language='en_US', digits=None, unitCode=None):
    """
    """
    if isinstance(code, dict):
        value = code.get('value', None)
        unitCode = code.get('unitCode', None)
    else:
        value=code


    if not unitCode:
        digits = '#' + str(digits) if digits else None
        result = format_decimal(value, locale=language, format=digits )
        return result

    try:
        ureg = UnitRegistry(auto_reduce_dimensions=True)
        value = value * ureg.parse_units(unitCode)    
        
        result = value.format_babel(locale=language)
        return result
    except Exception as e:
        return value

def _get_unitCode(code, language='en_US', digits=None, unitCode=None):
    """Returns unit of measure
    """
    if isinstance(code, dict):
        value = code.get('value', None)
        unitCode = code.get('unitCode', None)
    else:
        value=code


    if not unitCode:
        digits = '#' + str(digits ) if digits else None
        result = format_decimal(value, locale=language, format= digits )
        return result

    ureg = UnitRegistry(auto_reduce_dimensions=True)
    value = value * ureg.parse_units(unitCode)    

    result = value.units.format_babel(locale=language)
    return result
    


def _get_number2(code, language='en_US', digits=None, unitCode=None):
    """
    """
    if isinstance(code, dict):
        value = code.get('value', None)
        unitCode = code.get('unitCode', None)
    else:
        value=code

    digits = '#' + str(digits ) if digits else None
    result = format_decimal(value, locale=language, format= digits )


    return result + ' ' + str(unitCode) if unitCode else result

