
import copy
from kraken_localize.helpers import json
from kraken_localize.helpers import things
import os

from babel.dates import format_date, format_datetime, format_time
from babel.dates import format_timedelta
from babel.dates import get_timezone, UTC
import datetime
import functools







@functools.lru_cache(maxsize=128)
def get_delta(code, language, to=None, timezone='UTC'):
    """
    """
    if not to:
        to = datetime.datetime.now(datetime.timezone.utc)
        

    delta = to.astimezone(datetime.timezone.utc) - code.astimezone(datetime.timezone.utc)
    result = format_timedelta(delta, locale=language)
    
    return result
    

@functools.lru_cache(maxsize=128)
def get_date(code, language='en_us', timezone='UTC'):
    """
    """
    tz = get_timezone(timezone)

    if code.hour == 0 and code.minute == 0 and code.second == 0:
        new_code = code.astimezone(tz=tz)
        result = format_date(new_code, format='short', locale=language)
        return result
    else:
        print(tz)
        print('ss', code)
        new_code = code.astimezone(tz=tz)
        print('tt', new_code)
        result = format_datetime(new_code, format='short',  locale=language)
        return result


def utc_to_local(utc_dt, new_tz):
    return utc_dt.astimezone(tz=new_tz)

def local_to_utc(local_dt):
    return local_dt.astimezone(datetime.timezone.utc)
