#!/bin/bash
for Y in 2017 2018 2019
    do
        python3 aqi.py $Y-01-01 $Y-04-30
        python3 aqi.py $Y-05-01 $Y-08-31
        python3 aqi.py $Y-09-01 $Y-12-31
    done