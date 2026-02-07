import csv
import os
import mimetypes
from database import Database

def main():
    file_path = './file/import.csv'

    if not os.path.exists(file_path):
        print('Import file not found')
        return

    mime = mimetypes.guess_file_type(path=file_path)[0]
    if not mime in [
        'text/csv',
        'text/plain',
        'application/vnd.ms-excel',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    ]:
        print('Import file type not supported')
        return

    with open(file_path, 'r+') as csv_file:
        csv_lines = list(csv.reader(csv_file))

        print('Importing, please wait...\n')
        Database().import_csv(csv_lines)
        print('Successfully imported\n')


if __name__ == '__main__':
    main()