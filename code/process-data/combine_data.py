import pandas as pd 
import numpy as np

if __name__ == '__main__':
    air = pd.read_csv('../../data/processed/aggregated_aqi_daily_max.csv')
    bike = pd.read_csv('../../data/processed/aggregated_bikes_bsfa.csv')
    sta = pd.read_csv('../../data/processed/sta.csv')
    weather = pd.read_csv('../../data/processed/weather.csv')

    # join datasets

    bike['user_type_clean'] = np.where(bike['bike_share_for_all_trip'] == 'Yes', 'Subscriber - BSFA', 
        np.where((bike['user_type'] == 'Subscriber') & (bike['bike_share_for_all_trip'] == 'No'), 'Subscriber - Standard',
            'Customer'))
    bike = bike.drop(['user_type', 'bike_share_for_all_trip'], axis=1) 
    df = bike.merge(air, how='left', left_on='start_date', right_on='date')
    air_bike_size = df.shape[0]

    df = df.merge(sta, how='left', left_on='date', right_on='date_clean')
    air_bike_sta_size = df.shape[0]
    print(f'Size of new ({air_bike_sta_size}) same as old ({air_bike_size})? -> {air_bike_sta_size == air_bike_size}')


    df = df.merge(weather, how='left', left_on='date', right_on='time')
    air_bike_sta_weather_size = df.shape[0]
    print(f'Size of new ({air_bike_sta_weather_size}) same as old ({air_bike_size})? -> {air_bike_sta_weather_size == air_bike_size}')

    # cleanup fields
    df['sta'] = df['sta'].fillna(0)
    df_complete = df[~df['date'].isna()]
    print(f"shape of df_complete: {df_complete.shape}")
    df_complete = df_complete.drop(['date_clean', 'start_date', 'time', 'wpgt', 'tsun'], axis=1)
    df_complete['PM2.5'] = df_complete['PM2.5'].fillna(df_complete['PM2.5'].mean())
    df_complete['pres'] = df_complete['pres'].fillna(df_complete['pres'].mean())
    df_complete['snow'] = df_complete['snow'].fillna(df_complete['snow'].mean())
    df_complete['day_of_week'] = pd.to_datetime(df_complete['date']).dt.day_of_week
        # wpgt is peak wind gust, not captured
        # tsun is daily sunshine total, not captured
        # impute missing values with means

    rolling_cols = ['num_trips', 'avg_duration', 'max_aqi', 'max_aqi_category', 'CO', 'NO2', 'OZONE', 'PM2.5', 'tavg', 'tmin', 'tmax', 'wspd', 'pres']
    df_complete = df_complete.sort_values(['user_type_clean', 'date']).reset_index()
    df_complete_rolling = df_complete.drop('date', axis=1) \
        .groupby(['user_type_clean', 'day_of_week']) \
        .rolling(window=9, center=True).mean() \
        .reset_index()

    df_complete_rolling.set_index('level_2', inplace=True)
    df_complete_rolling.sort_index(inplace=True)

    residuals = (df_complete[rolling_cols] - df_complete_rolling[rolling_cols]) / df_complete_rolling[rolling_cols]
    residuals = residuals.add_suffix('_res')

    df_complete_residuals = df_complete.merge(residuals, left_index=True, right_index=True) \
        .dropna()
    print(f"Shape of final dataset: {df_complete_residuals.shape}")
    df_complete.to_csv('../../data/final/final_data_bsfa.csv', index=False)