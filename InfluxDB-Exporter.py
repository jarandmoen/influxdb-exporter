#!/usr/bin/python3

"""
InfluxDB Data Exporter

This script facilitates the extraction of time series data from InfluxDB, allowing for data output in either JSON or CSV format. It provides options to specify the date range for the data extraction, the desired output format, and whether the data should be chunked into hourly intervals.

Features include:
- Command-line arguments for setting up database parameters and data extraction specifics.
- Validation of date inputs.
- Option to export data in hourly chunks or daily aggregates.
- Ability to choose between JSON or CSV output formats.
- Checking for existing files to prevent overwriting.

Author: Jarand Moen and GPT-4
Creation Date: November 9, 2023
Version: 1.0

License:
This script is released under the "Free for All" license, which is a permissive, non-copyleft open source license. It permits users to do anything they wish with the code, without limitations, and requires no attribution or inclusion of the license itself. This means you may use, modify, distribute, and sublicense this code however you like, for commercial or non-commercial purposes, without restriction.

This script is provided "as is", without warranty of any kind, express or implied. In no event shall the authors or copyright holders be liable for any claim, damages, or other liability arising from the use of the software.
"""

import json
import csv
import gc
import os
import argparse
from datetime import datetime, timedelta
from influxdb import InfluxDBClient

# Parse command line arguments
parser = argparse.ArgumentParser(description='Extract data from InfluxDB.')
parser.add_argument('--database', required=True, help='The name of the InfluxDB database')
parser.add_argument('--measurement', required=True, help='The name of the measurement to extract data from')
parser.add_argument('--start', required=True, help='Start date in YYYY-MM-DD format')
parser.add_argument('--end', required=True, help='End date in YYYY-MM-DD format')
parser.add_argument('--hourly', action='store_true', help='Export data in hourly chunks (optional)')
parser.add_argument('--host', default='localhost', help='The InfluxDB host to connect to (default: localhost)')
parser.add_argument('--port', default=8086, type=int, help='The InfluxDB port to connect to (default: 8086)')
parser.add_argument('--output-format', default='json', choices=['json', 'csv'], help='The output format of the data (default: json)')

args = parser.parse_args()

# Validate the provided dates
try:
    start_date = datetime.strptime(args.start, '%Y-%m-%d')
    end_date = datetime.strptime(args.end, '%Y-%m-%d')
except ValueError:
    print("Invalid date format. Please use YYYY-MM-DD.")
    exit(1)

# Setup InfluxDB connection
client = InfluxDBClient(host=args.host, port=args.port)
client.switch_database(args.database)

# Function to fetch and save data
def fetch_and_save_data(start_time, end_time):
    # Construct the InfluxQL query
    query = f'SELECT * FROM {args.measurement} WHERE time >= \'{start_time}\' AND time < \'{end_time}\''

    # Execute the query and fetch the results
    result = client.query(query)
    points = list(result.get_points())

    # Check if the points list is empty
    if not points:
        print(f'No data found for {args.measurement} between {start_time} and {end_time}. Skipping file creation.')
        return

    # Output data according to specified format
    time_format = "%Y_%m_%d_%H" if args.hourly else "%Y_%m_%d"
    filename_prefix = f'data_{args.measurement}_{start_time.strftime(time_format)}'

    # Check if file already exists to prevent overwriting
    if args.output_format == 'json':
        filename = f'{filename_prefix}.json'
    elif args.output_format == 'csv':
        filename = f'{filename_prefix}.csv'

    # Now check if the file exists
    if os.path.exists(filename):
        print(f'Error: The file {filename} already exists. Data not saved for this period.')
        return

    # Continue with file writing only if file does not exist
    if args.output_format == 'json':
        with open(filename, 'w') as f:
            json.dump(points, f, indent=4)
    elif args.output_format == 'csv':
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=points[0].keys())
            writer.writeheader()
            writer.writerows(points) 

    print(f'Data from {args.database}.{args.measurement} extracted and saved to {args.output_format.upper()} file {filename}.')

    # Garbage collect
    del result
    del points
    gc.collect()

# Loop over each day in the range and fetch the data from InfluxDB
current_date = start_date

print('Starting Export.')

while current_date <= end_date:
    if args.hourly:
        # If hourly chunks are requested, split each day into hours
        for hour in range(24):
            start_time = current_date + timedelta(hours=hour)
            end_time = start_time + timedelta(hours=1)
            fetch_and_save_data(start_time, end_time)
    else:
        # Otherwise, process the entire day
        start_time = current_date
        end_time = current_date + timedelta(days=1)
        fetch_and_save_data(start_time, end_time)

    # Move to the next day
    current_date += timedelta(days=1)

print('Done!')
