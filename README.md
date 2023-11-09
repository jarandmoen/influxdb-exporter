# InfluxDB Data Exporter

This script facilitates the extraction of time series data from InfluxDB, allowing for data output in either JSON or CSV format. It provides options to specify the date range for the data extraction, the desired output format, and whether the data should be chunked into hourly intervals.

NOTE: This script only exports measurements inside a database, as defined as an argument.

## Features include
- Command-line arguments for setting up database parameters and data extraction specifics.
- Option to export data in hourly or daily chunks.
- Ability to choose between JSON or CSV output formats.
- Checking for existing files to prevent overwriting.
- Error messaging for empty data sets or file existence.

## Installing Dependencies
Install the required packages using pip:
```pip install influxdb argparse```

This will install the influxdb client library needed to interact with the InfluxDB instance and argparse for parsing command-line options (though argparse should be included in the Python Standard Library for Python 3.2 and later).

## Usage
To use the script, you can provide the necessary information as command-line arguments. Here is an example command:

```python3 InfluxDB-Exporter.py --database mydatabase --measurement mymeasurement --start 2021-01-01 --end 2021-01-02 --output-format=json```

You can also include optional arguments for hourly exports, InfluxDB host, port, username, and password:

```python3 InfluxDB-Exporter.py --database mydatabase --measurement mymeasurement --start 2021-01-01 --end 2021-01-02 --output-format=csv --hourly --host localhost --port 8086 --username myuser --password mypassword```

Replace mydatabase, mymeasurement, myuser, and mypassword with your actual database name, measurement name, username, and password respectively.

## Version
Creation Date: November 9, 2023

Version: MIT

## License:
This script is released under the "Free for All" license, which is a permissive, non-copyleft open source license. It permits users to do anything they wish with the code, without limitations, and requires no attribution or inclusion of the license itself. This means you may use, modify, distribute, and sublicense this code however you like, for commercial or non-commercial purposes, without restriction.

This script is provided "as is", without warranty of any kind, express or implied. In no event shall the authors or copyright holders be liable for any claim, damages, or other liability arising from the use of the software.
