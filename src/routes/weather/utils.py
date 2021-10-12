from services.time import date, get_first_day_of_month_and_next, tommororow


def get_interval_query(start: str, end: str = None):
    if start is not None:
        if end is not None:
            return f"timestamp >= '{date(start)}' AND timestamp <= '{tommororow(date(end))}'"
        return f"timestamp >= '{date(start)}'"

    if end is not None:
        return f"timestamp <= '{tommororow(date(end))}'"

    return None


def get_month_measurements_query(month, year):
    [this_month, next_month] = get_first_day_of_month_and_next(month, year)
    return f"timestamp < '{next_month}' AND timestamp >= '{this_month}'"
