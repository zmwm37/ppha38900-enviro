import pandas as pd 
import numpy as np

if __name__ == '__main__':
    air = pd.read_csv('../../data/processed/aggregated_aqi_daily_max.csv')
    bike = pd.read_csv('../../data/processed/aggregated_bikes.csv')
    sta = pd.read_csv('../../data/processed/sta.csv')
    weather = pd.read_csv('../../data/processed/weather.csv')

    # join datasets
    df = air.merge(bike, how='left', left_on='date', right_on='start_date')
    air_bike_size = df.shape[0]

    df = df.merge(sta, how='left', left_on='date', right_on='date_clean')
    air_bike_sta_size = df.shape[0]
    print(f'Size of new ({air_bike_sta_size}) same as old ({air_bike_size})? -> {air_bike_sta_size == air_bike_size}')


    df = df.merge(weather, how='left', left_on='date', right_on='time')
    air_bike_sta_weather_size = df.shape[0]
    print(f'Size of new ({air_bike_sta_weather_size}) same as old ({air_bike_size})? -> {air_bike_sta_weather_size == air_bike_size}')

    # cleanup fields
    df['sta'] = df['sta'].fillna(0)
    df_complete = df[~df['start_date'].isna()]
    df_complete = df_complete.drop(['date_clean', 'wpgt', 'tsun'], axis=1)

    # add additional fields
    # TODO - makes fields for time t-1
    # TODO - adjust seasonal fields to get rolling window residuals
    print("WARNING - CODE HAS SOME TODOS")
    df_complete.to_csv('../../data/final/final_data.csv', index=False)