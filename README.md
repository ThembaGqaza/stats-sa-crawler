# Stats SA Data Extraction Script

This repository contains a Python-based script designed to extract and collect census data from the Stats SA (Statistics South Africa) API. The script efficiently loops through all provinces, districts, and municipalities, pulling data across multiple tables and saving the results to CSV files.

## Features

- **API Integration**: Extracts data directly from the Stats SA API using `requests` for seamless data access.
- **Multiple Report Types**: Collects data across various demographic categories such as age groups, population groups, sexes, languages, education levels, and more.
- **Scalable and Efficient**: Uses progress bars (`tqdm`) to provide feedback on the status of data extraction at the provincial and table levels, allowing for large-scale data collection.
- **Filtered Data**: Automatically filters out unnecessary columns (e.g., columns ending with 'String') to ensure clean and relevant datasets.
- **Data Output**: Saves extracted data in CSV format, organizing it by report type for each combination of province, district, and municipality.
- **Error Handling**: Built-in `try` and `except` blocks handle errors gracefully during API requests and file operations.

## Requirements

All dependencies are installed via the `requirements.txt` file located in the repository. To install them, simply run:

`pip install -r requirements.txt
`


## How It Works

1. **Fetches Data**: The script connects to the Stats SA API to retrieve data for each combination of province, district, and municipality.
2. **Extracts Multiple Reports**: It pulls data for various tables including age groups, population groups, education levels, and more.
3. **Processes and Saves Data**: After filtering the relevant columns, the data is saved to CSV files, one for each report type, in a designated `data/` folder.

## Usage

Simply run the script from the terminal as follows:

`
python extractor.py
`


You can monitor progress in the terminal with the displayed status bars, indicating the processing of provinces and tables.

## Report Types Extracted

The script pulls data from the following categories:

- Age Groups
- Population Groups
- Sexes
- Languages
- Highest Level of Education
- Type of Main Dwellings
- Access to Piped Water
- Main Toilet Facility
- Refuse Disposal
- Energy for Cooking
- School Attendance

Each report is saved in a separate CSV file, named after the report type (e.g., `DsAgeGroups_report.csv`, `DsPopulationGroups_report.csv`).

## Error Handling

If an error occurs during data retrieval or saving, the script will continue to process the remaining data, logging any issues for further inspection.

## Contributing

Feel free to open issues or submit pull requests to contribute to this project.
