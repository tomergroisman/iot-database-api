import io
from datetime import datetime
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


def get_weather_measurements_plot():
    measurements_dict = {
        "times": [],
        "temperatures": [],
        "humidities": [],
        "heat_indexes": []
    }

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
    axis.scatter(measurements_dict["times"], measurements_dict["temperatures"], s=5)
    axis.scatter(measurements_dict["times"], measurements_dict["humidities"], s=5)
    axis.scatter(measurements_dict["times"], measurements_dict["heat_indexes"], s=5)

    axis.set_xlim([0, 24])
    axis.set_ylim([0, 100])

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)

    return output.getvalue()
