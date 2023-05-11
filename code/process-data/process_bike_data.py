import pandas as pd
import numpy as np
from utils import *

if __name__ == "__main__":
    file_path = '../../data/raw/bike-trips/'
    sc = ['duration_sec', 'start_time', 'end_time', 'user_type']
    df_combo, err = feed_bike_files(file_path=file_path, selected_cols=sc, v=0)
    df_combo.to_csv('../../data/processed/aggregated_bikes.csv')