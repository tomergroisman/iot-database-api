import matplotlib.pyplot as plt
import requests

from utils import timestamp_to_dec

API_ENDPOINT = "http://10.100.102.21:3000/weather"
measurements = requests.get(API_ENDPOINT).json()

measurements_dict = {
    "times": [],
    "temperatures": [],
    "humidities": [],
    "heat_indexes": []
}

for measurement in measurements:
    time = timestamp_to_dec(measurement["timestamp"])
    temperature = measurement["temperature"]
    humidity = measurement["humidity"]
    heat_index = measurement["heat_index"]

    measurements_dict["times"].append(time)
    measurements_dict["temperatures"].append(temperature)
    measurements_dict["humidities"].append(humidity)
    measurements_dict["heat_indexes"].append(heat_index)

plt.scatter(measurements_dict["times"], measurements_dict["temperatures"], s=5)
plt.scatter(measurements_dict["times"], measurements_dict["humidities"], s=5)
plt.scatter(measurements_dict["times"], measurements_dict["heat_indexes"], s=5)

plt.xlim([0, 24])
plt.ylim([0, 100])
plt.show()
