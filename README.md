# query_app_lokesh

## Overview
This project is a data query tool built with Python, PySide2, and PostgreSQL. It allows users to interactively select a CSV file containing electric vehicle population data, create a database table based on the CSV headers, and fetch specific data from the PostgreSQL database.

## Requirements
To run this project, you need to have the following installed:

- Python 3.7 or higher
- PySide2
- pandas
- psycopg2

You can install the necessary packages using pip:

```bash
pip install PySide2 pandas psycopg2
```
## Installation
### Clone this repository to your local machine:
```bash
git clone https://github.com/lokesh6618/query_app_lokesh
```
### Navigate to the project directory:
```bash
cd query_app_lokesh
```

## Running the Application
```bash
python main.py
```

## Running Tests
```bash
python -m unittest tests.unittests.test_db_connect.TestDbConnect
```
### Running a Specific Test

```bash
python3 -m unittest tests.unittests.test_db_connect.TestDbConnect.test_add_data_from_data_frame
```
