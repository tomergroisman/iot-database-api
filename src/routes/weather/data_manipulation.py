import numpy as np
import warnings

warnings.simplefilter('ignore')


def values_to_time_bins(measurements):
    bins = [[] for i in range(48)]
    for measurement in measurements:
        timestamp = measurement.get('timestamp')
        if timestamp:
            bin_index = _get_bin_index(timestamp.hour, timestamp.minute)
            bins[bin_index].append(measurement)
    return bins


def calculate_average(measurements):
    return _calculate(measurements, np.mean)


def calculate_median(measurements):
    return _calculate(measurements, np.median)


def _calculate(measurements, func):
    bins = values_to_time_bins(measurements)
    temperatures, humidities, heat_indexes = [], [], []
    for measurements in bins:
        temperatures.append(func([measurement.get('temperature') for measurement in measurements]))
        humidities.append(func([measurement.get('humidity') for measurement in measurements]))
        heat_indexes.append(func([measurement.get('heat_index') for measurement in measurements]))
    return {
        'temperatures': temperatures,
        'humidities': humidities,
        'heat_indexes': heat_indexes
    }


def _get_bin_index(hour, minute):
    if minute < 15:
        return hour * 2
    if minute < 45:
        return (hour * 2) + 1
    return ((hour + 1) * 2) % 48
