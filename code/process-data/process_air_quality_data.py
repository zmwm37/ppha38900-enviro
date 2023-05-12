import pandas as pd 
import numpy as np
import os
from utils import *

# from AirNowAPI documentation
# Outputs: https://docs.airnowapi.org/Data/docs
header_cols = ['lat', 'lon', 'utc', 'parameter','concentration', 'unit', 'raw_concentration',
    'aqi', 'aqi_category', 'site_name', 'site_agency', 'aqs_id', 'full_aqs_id']
file_path = '../../data/raw/air-quality/'

df_daily_max, error_log = feed_aqi_files(file_path, header_cols=header_cols, v=0)
if len(error_log) > 0:
    print("WARNING - the following files could not be processed:")
    for e in error_log:
        print(f'{e} \n')
df_daily_max.to_csv('../../data/processed/aggregated_aqi_daily_max.csv', index=False)