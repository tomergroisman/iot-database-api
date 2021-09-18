import io
import datetime as dt
from datetime import datetime
from flask import request
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from services.postgres import get_instances
from .constants import (
    WEATHER_DB_NAME as db_name,
    WEATHER_TABLE_NAME as table_name,
)


def timestamp_to_dec(timestamp: datetime):
    hour, minute, second = timestamp.strftime("%H:%M:%S").split(":")
    time = int(hour) + int(minute) / 60 + int(second) / 6000
    return time


def today():
    return dt.date.today()


def tommororow(date: datetime = None):
    if date is None:
        return today() + dt.timedelta(1)
    yyyy, mm, dd = date.split('-')
    date = dt.datetime(int(yyyy), int(mm), int(dd))
    return date + dt.timedelta(1)


def get_weather_measurements_plot():
    measurements_dict = {
        "times": [],
        "temperatures": [],
        "humidities": [],
        "heat_indexes": []
    }

    scope = request.args.get('scope')
    plot = request.args.get('plot', 'scatter')

    measurements_scope = {
        'today': get_instances(db_name, table_name, None, f"timestamp >= '{today()}' AND timestamp < '{tommororow()}'"),
        None: get_instances(db_name, table_name, None, None)
    }

    measurements = measurements_scope.get(scope)
    if measurements is None:
        measurements = get_instances(
            db_name,
            table_name,
            None,
            f"timestamp >= '{scope}' AND timestamp < '{tommororow(scope)}'"
        )

    for measurement in measurements:
        time = timestamp_to_dec(measurement["timestamp"])
        temperature = measurement["temperature"]
        humidity = measurement["humidity"]
        heat_index = measurement["heat_index"]

        measurements_dict["times"].append(time)
        measurements_dict["temperatures"].append(temperature)
        measurements_dict["humidities"].append(humidity)
        measurements_dict["heat_indexes"].append(heat_index)

    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    if plot == 'line':
        axis.plot(measurements_dict["times"], measurements_dict["temperatures"], label='Temperature')
        axis.plot(measurements_dict["times"], measurements_dict["humidities"], label='Humidity')
        axis.plot(measurements_dict["times"], measurements_dict["heat_indexes"], label='Heat Index')
    if plot == 'scatter':
        axis.scatter(measurements_dict["times"], measurements_dict["temperatures"], s=5, label='Temperature')
        axis.scatter(measurements_dict["times"], measurements_dict["humidities"], s=5, label='Humidity')
        axis.scatter(measurements_dict["times"], measurements_dict["heat_indexes"], s=5, label='Heat Index')

    axis.legend()
    axis.set_xlim([0, 24])
    axis.set_ylim([0, 100])

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)

    return output.getvalue()
