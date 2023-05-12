import pandas as pd
import numpy as np
import os

def aggregate_bike_df(df: pd.DataFrame) -> pd.DataFrame:
    df_agg = df.groupby(['start_date', 'user_type']) \
        .agg(num_trips = ("duration_sec", "count"),
            avg_duration = ("duration_sec",'mean')) \
        .reset_index()
    return df_agg

def clean_bike_fields(df: pd.DataFrame) -> pd.DataFrame:
    df['start_time_dt'] = pd.to_datetime(df['start_time'])
    df['end_time_dt'] = pd.to_datetime(df['end_time'])
    df['start_date'] = df['start_time_dt'].dt.date
    return df

def feed_bike_files(file_path: str, selected_cols: list, v: int) -> tuple[pd.DataFrame, list]:
    '''
    Process and combine files from specified file_path

    Inputs: 
        file_path: the directory where files to be processed are located
        selected_cols: which variables in the dataframe are required from each file
        v: verbosity level (0=None, 1=All)

    Outputs:
        combined dataframe and list of files that could not be processed.
    '''
    files =  os.listdir(file_path)
    df_combo = pd.DataFrame()
    error_log = []    
    for i, f in enumerate(files):
        if v > 0:
            print(f"PROCESS FILE {i}: {f}")
        try:
            df = pd.read_csv(file_path + f)
        except:
            print(f"WARNING - could not read file {f}")
            error_log.append(f)
            continue
        try:
            df = df[selected_cols]
        except:
            print(f"WARNING - required columns are not present in {f}")
            error_log.append(f)
            continue
        df_clean = clean_bike_fields(df)
        df_agg = aggregate_bike_df(df_clean)
        df_combo = pd.concat([df_combo, df_agg])

    return (df_combo, error_log)

def clean_aqi_data(df:pd.DataFrame) -> pd.DataFrame:
    df['date'] = pd.to_datetime(df['utc']).dt.date
    return df

def aggregate_measures_data(df:pd.DataFrame) -> pd.DataFrame:
    df_agg = df.groupby(['date', 'parameter']) \
        .agg(max_daily_concentration = ('raw_concentration', 'max')) \
        .reset_index()
    return df_agg

def make_measures_agg_wide(df:pd.DataFrame) -> pd.DataFrame:
    df_wide = df.pivot(index='date', columns='parameter') \
    .reset_index()
    df_wide.columns = df_wide.columns.droplevel(0)
    df_wide  = df_wide.rename(columns={'':'date'})
    return df_wide

def make_quality_split(df):
    df_aqi = df[['date', 'aqi', 'aqi_category']]
    df_agg_aqi = df_aqi.groupby('date') \
        .agg(max_aqi = ('aqi', 'max'),
            max_aqi_category = ('aqi_category', 'max')) \
        .reset_index()
    return df_agg_aqi

def feed_aqi_files(file_path:str, header_cols: list, v:int) -> tuple[pd.DataFrame, list]:
    files =  os.listdir(file_path)
    df_combo = pd.DataFrame()
    error_log = []
    for i, f in enumerate(files):
        if v > 0 :
            print(f"PROCESS FILE {i}: {f}")
        try:
            df = pd.read_csv(file_path + f, names=header_cols)
        except:
            print(f"WARNING - could not read file {f}")
            error_log.append(f)
            continue
        df_clean = clean_aqi_data(df)
        df_agg_measures = aggregate_measures_data(df_clean)
        # print(f"df_agg_measures : \n {df_agg_measures.head()}")
        # print(f"df_agg_measures columns: {df_agg_measures.columns}")
        # print(f"missing parameter {sum(df_agg_measures['parameter'].isna())}")
        df_agg_measures_wide = make_measures_agg_wide(df_agg_measures)
        df_agg_aqi = make_quality_split(df_clean)
        df_agg = df_agg_aqi.merge(df_agg_measures_wide, how='left', on='date') 

        df_combo = pd.concat([df_combo, df_agg])
    
    return (df_combo, error_log)