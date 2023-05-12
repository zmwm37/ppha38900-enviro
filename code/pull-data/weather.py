from datetime import datetime
from meteostat import Stations, Daily
import numpy as np
import pandas as pd



if __name__=='__main__':
    sfo_lat = 37.61961
    sfo_lon = -122.36558
    start = datetime(2017, 6, 28)
    end = datetime(2019, 12, 31)
    Stations = Stations()
    stations = Stations.nearby(sfo_lat, sfo_lon)
    nearest_station = stations.fetch(5).reset_index()
    nearest_id = nearest_station['id'][0]
    nearest_name = nearest_station['name'][0]
    sfo_data = Daily(nearest_id, start, end)
    sfo_data = sfo_data.fetch().reset_index()
    sfo_data.to_csv('../../data/processed/weather.csv', index=False)
    print(f'Downloaded data from {nearest_name} (id: {nearest_id}) from {start.date()} to {end.date()}')