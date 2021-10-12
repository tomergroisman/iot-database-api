import io
from flask import request
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from routes.weather.utils import get_interval_query

from services.postgres import get_instances
from services.time import today, tommororow, timestamp_to_dec
from .constants import (
    WEATHER_DB_NAME as db_name,
    WEATHER_TABLE_NAME as table_name,
)


def get_weather_measurements_plot():
    measurements_dict = {
        "times": [],
        "temperatures": [],
        "humidities": [],
        "heat_indexes": []
    }

    scope = request.args.get('scope')
    start = request.args.get('start')
    end = request.args.get('end')
    plot = request.args.get('plot', 'scatter')

    measurements_scope = {
        'today': {
            "db_name": db_name,
            "table_name": table_name,
            "columns": None,
            "filter_query": f"timestamp >= '{today()}' AND timestamp < '{tommororow()}'"
        }
    }

    measurements = None

    if scope is not None:
        measurements = get_instances(**measurements_scope.get(scope))
    else:
        measurements = get_instances(
            db_name,
            table_name,
            None,
            get_interval_query(start, end)
        )

    if measurements is None:
        measurements = get_instances(db_name, table_name, None, None)

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


def get_manipulated_data_plot(data, plot='line'):
    times = [i / 2 for i in range(48)]

    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    if plot == 'line':
        axis.plot(times, data["temperatures"], label='Temperature')
        axis.plot(times, data["humidities"], label='Humidity')
        axis.plot(times, data["heat_indexes"], label='Heat Index')
    if plot == 'scatter':
        axis.scatter(times, data["temperatures"], s=5, label='Temperature')
        axis.scatter(times, data["humidities"], s=5, label='Humidity')
        axis.scatter(times, data["heat_indexes"], s=5, label='Heat Index')

    axis.legend()
    axis.set_xlim([0, 24])
    axis.set_ylim([0, 100])

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)

    return output.getvalue()
