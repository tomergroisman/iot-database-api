from datetime import datetime


def timestamp_to_dec(timestamp: str):
    date = datetime.strptime(timestamp, '%a, %d %b %Y %H:%M:%S GMT')
    time = date.hour + date.minute / 60 + date.second / 6000
    return time
