## About
This application will import csv file to SQL database

Mysql, postgres and sqlite are supported
## How to run

Open terminal

Create and activate virtual environment

```
python -m venv .venv
source .venv/bin/activate
```

Install required libraries (only dotenv is required)

```
pip install -m requirements.txt
```

Copy .env.dist to .env file and add your credentials
```
cp .env.dist .env
```

Run main.py

```
python main.py
```

## Instructions
Put csv file to file directory, and name it import.csv
I file contains heder, application will automatically map header lines to db columns.
Header line can be defined in config module. If defined that definition will be used instead of file's title line, 
or if title line is missing. If both present, config will take priority

NOTE that database and table must exist before import is executed, application won't create them (except for sqlite, 
where table will be created).