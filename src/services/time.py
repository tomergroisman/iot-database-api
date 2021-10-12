import datetime as dt
from datetime import datetime


def timestamp_to_dec(timestamp: datetime):
    hour, minute, second = timestamp.strftime("%H:%M:%S").split(":")
    time = int(hour) + int(minute) / 60 + int(second) / 6000
    return time


def date(timetamp: str):
    return datetime.strptime(timetamp, '%d-%m-%Y')


def today():
    return dt.date.today()


def tommororow(date: datetime = None):
    if date is None:
        return today() + dt.timedelta(1)
    return date + dt.timedelta(1)
