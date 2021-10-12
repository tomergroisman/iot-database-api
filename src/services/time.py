import datetime as dt
from datetime import datetime


def timestamp_to_dec(timestamp: datetime):
    hour, minute, second = timestamp.strftime("%H:%M:%S").split(":")
    time = int(hour) + int(minute) / 60 + int(second) / 6000
    return time


def date(timetamp: str):
    return datetime.strptime(timetamp, '%d-%m-%Y')


def get_first_day_of_month(month: int, year: int):
    return date(f"01-{month}-{year}")


def get_first_day_of_month_and_next(month: int, year: int):
    month_datetime = get_first_day_of_month(month, year)
    if month < 12:
        next_datetime = get_first_day_of_month(month + 1, year)
    else:
        next_datetime = get_first_day_of_month(1, year + 1)
    print([month_datetime, next_datetime])
    return [month_datetime, next_datetime]


def today():
    return dt.date.today()


def tommororow(date: datetime = None):
    if date is None:
        return today() + dt.timedelta(1)
    return date + dt.timedelta(1)
