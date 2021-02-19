import pandas as pd


def generate_trip_id(gps):
    gps['trip_id'] = gps['date'].astype('str') + ' ' + gps['vehicle_id']
    return gps

def generate_point_id(gps):
    gps['point_id'] = gps['datetime'].astype('str') + ' ' + gps['vehicle_id']
    return gps