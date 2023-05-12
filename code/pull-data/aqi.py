import os
import sys
from datetime import datetime
from os.path import expanduser
from datetime import datetime
import requests

def main():
    
    # API parameters
    try:
        len(sys.argv) == 3
    except:
        print('''
            USAGE: start and end date must be provided as CLI aruguments in format YYYY-DD-MM \n
            Example: python aqi.py 2023-01-01 2023-01-05
        ''')
    
    start_date = sys.argv[1]
    end_date = sys.argv[2]
    options = {}
    options["url"] = "https://airnowapi.org/aq/data/"
    options["start_date"] = start_date
    options["start_hour_utc"] = "0"
    options["end_date"] = end_date
    options["end_hour_utc"] = "23"
    options["parameters"] = "o3,pm25,pm10,co,no2,so2"
    options["bbox"] = "-122.45, 37.6,-122.35,37.78" # SF + Oakland
    options["data_type"] = "b"
    options["format"] = "text/csv"
    options["verbose"] = "1"
    options["includerawconcentrations"] = "1"
    options["ext"] = "csv"
    options["api_key"] = "5FA2B7E1-7E58-4DBF-81C7-6BDB7D33085D"

    # API request URL
    REQUEST_URL = options["url"] \
                  + "?startdate=" + options["start_date"] \
                  + "t" + options["start_hour_utc"] \
                  + "&enddate=" + options["end_date"] \
                  + "t" + options["end_hour_utc"] \
                  + "&parameters=" + options["parameters"] \
                  + "&bbox=" + options["bbox"] \
                  + "&datatype=" + options["data_type"] \
                  + "&format=" + options["format"] \
                  + "&api_key=" + options["api_key"] \
                  + "&verbose=" + options["verbose"] \
                  + "&includerawconcentrations=" + options["includerawconcentrations"] 

    try:
        # Request AirNowAPI data
        print("Requesting AirNowAPI data...")

        # Perform the AirNow API data request
        #api_data = urllib.request.urlopen(REQUEST_URL)
        #with urllib.request.urlopen(REQUEST_URL) as f:
        #    print(f.read(10))
        ###
        # WITH REQUESTS LIBRARY
        req = requests.get(REQUEST_URL)
        url_content = req.content
        timestamp =datetime.now()
        csv_file = open(f'../../data/raw/air-quality/aqi_download_{start_date}_{end_date}.csv', 'wb')
        csv_file.write(url_content)
        csv_file.close()
        ###

        # Download complete
        print(f"Download URL: {REQUEST_URL}")

    except Exception as e:
        print(f"Unable perform AirNowAPI request. {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()