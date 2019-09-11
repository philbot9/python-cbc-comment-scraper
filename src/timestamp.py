from datetime import datetime


def now():
    dt_now = datetime.now()
    ts = datetime.timestamp(dt_now)
    return round(ts)
