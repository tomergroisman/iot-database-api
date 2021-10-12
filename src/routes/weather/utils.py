from services.time import date, tommororow


def get_interval_query(start: str, end: str = None):
    if start is not None:
        if end is not None:
            return f"timestamp >= '{date(start)}' AND timestamp <= '{tommororow(date(end))}'"
        return f"timestamp >= '{date(start)}'"

    if end is not None:
        return f"timestamp <= '{tommororow(date(end))}'"

    return None
