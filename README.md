# influxdb-exporter
InfluxDB Data Exporter

This script facilitates the extraction of time series data from InfluxDB, allowing for data output in either JSON or CSV format. It provides options to specify the date range for the data extraction, the desired output format, and whether the data should be chunked into hourly intervals.

Features include:
- Command-line arguments for setting up database parameters and data extraction specifics.
- Validation of date inputs.
- Option to export data in hourly chunks or daily aggregates.
- Ability to choose between JSON or CSV output formats.
- Checking for existing files to prevent overwriting.
- Error messaging for empty data sets or file existence.

Creation Date: November 9, 2023
Version: 1.0

License:
This script is released under the "Free for All" license, which is a permissive, non-copyleft open source license. It permits users to do anything they wish with the code, without limitations, and requires no attribution or inclusion of the license itself. This means you may use, modify, distribute, and sublicense this code however you like, for commercial or non-commercial purposes, without restriction.

Note:
This license is not recognized by the Open Source Initiative (OSI) or the Free Software Foundation (FSF). It's intended for educational purposes and small personal projects. It's always recommended to consult with a legal expert or to use OSI-approved licenses for larger projects or those involving distribution.

This script is provided "as is", without warranty of any kind, express or implied. In no event shall the authors or copyright holders be liable for any claim, damages, or other liability arising from the use of the software.
