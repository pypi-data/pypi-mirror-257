import holidays as _holidays
import datetime as _datetime


def market_open(now, prepost=False):
    if prepost:
        return _datetime.time(7,30,0) < now.time() < _datetime.time(16,0,0)\
           and now.weekday() not in (5, 6)\
           and now.date() not in _holidays.US()
    else:
        return _datetime.time(8,30,0) < now.time() < _datetime.time(15,0,0)\
           and now.weekday() not in (5, 6)\
           and now.date() not in _holidays.US()