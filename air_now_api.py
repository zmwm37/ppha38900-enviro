import os
import sys
from datetime import datetime
from os.path import expanduser
#import urllib.request
import requests

def main():

    # API parameters
    options = {}
    options["url"] = "https://airnowapi.org/aq/data/"
    options["start_date"] = "2014-09-23"
    options["start_hour_utc"] = "22"
    options["end_date"] = "2014-09-23"
    options["end_hour_utc"] = "23"
    options["parameters"] = "o3,pm25"
    options["bbox"] = "-90.806632,24.634217,-71.119132,45.910790"
    options["data_type"] = "a"
    options["format"] = "text/csv"
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
                  + "&api_key=" + options["api_key"]

    try:
        # Request AirNowAPI data
        print("Requesting AirNowAPI data...")

        # User's home directory.
        home_dir = expanduser("~")
        download_file_name = "AirNowAPI" + datetime.now().strftime("_%Y%M%d%H%M%S." + options["ext"])
        download_file = os.path.join(home_dir, download_file_name)

        # Perform the AirNow API data request
        #api_data = urllib.request.urlopen(REQUEST_URL)
        #with urllib.request.urlopen(REQUEST_URL) as f:
        #    print(f.read(10))
        ###
        # WITH REQUESTS LIBRARY
        req = requests.get(REQUEST_URL)
        url_content = req.content
        csv_file = open('aqi_download.csv', 'wb')
        csv_file.write(url_content)
        csv_file.close()
        ###

        # Download complete
        print(f"Download URL: {REQUEST_URL}")
        print(f"Download File: {download_file}") 

    except Exception as e:
        print(f"Unable perform AirNowAPI request. {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()