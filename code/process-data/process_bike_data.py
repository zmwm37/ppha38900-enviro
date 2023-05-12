import pandas as pd
import numpy as np
from utils import *
import sys

if __name__ == "__main__":
    file_path = '../../data/raw/bike-trips/'
    if len(sys.argv) > 1:
        mode = sys.argv[1]
    else:
        mode = None
    if mode == 'bsfa':
        sc = ['duration_sec', 'start_time', 'end_time', 'user_type', 'bike_share_for_all_trip']
    else:
        sc = ['duration_sec', 'start_time', 'end_time', 'user_type']
    df_combo, err = feed_bike_files(file_path=file_path, selected_cols=sc, mode=mode, v=0)
    if mode == 'bsfa':
        df_combo.to_csv('../../data/processed/aggregated_bikes_bsfa.csv', index=False)
    else:
        df_combo.to_csv('../../data/processed/aggregated_bikes.csv', index=False)