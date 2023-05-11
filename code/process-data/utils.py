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
        df = pd.read_csv(file_path + f)
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