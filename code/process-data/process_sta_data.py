import pandas as pd
import numpy as np
from utils import *

if __name__ == '__main__':
    df = pd.read_csv('../../data/raw/spare_the_air_raw.csv')
    df_2017_2019 = df[(df['Year'].astype(int) > 2016) & (df['Year'].astype(int) < 2020)]
    df_2017_2019 = df_2017_2019[df_2017_2019['Date'] != '0']

    df_2017_2019 = pd.concat([df_2017_2019, df_2017_2019['Date'].str.split(',', expand=True)], axis=1)
    df_2017_2019 = df_2017_2019.rename({0:'weekday', 1:'md'}, axis='columns')
    df_2017_2019['Year'] = df_2017_2019['Year'].astype(str)
    df_2017_2019['md'] = df_2017_2019['md'].str.strip()
    df_2017_2019['mdy'] = df_2017_2019['md'].str.cat(df_2017_2019['Year'], sep=',')
    df_2017_2019['date_clean'] = pd.to_datetime(df_2017_2019['mdy'], format='%B %d,%Y')
    df_2017_2019['sta'] = 1
    df_2017_2019[['date_clean', 'sta']].to_csv('../../data/processed/sta.csv', index=False)