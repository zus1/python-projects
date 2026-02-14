import os
import csv
import magic

from config import Config
from clients import Aws

class Source:
    def __init__(self):
        self.__source = Config.get_csv_source()

    def read_from_source(self)->list[tuple]:
        return getattr(self, f'{self.__source}')()

    def local(self)->list[tuple]:
        print('Importing from local...')
        file_path = 'file/example.csv'

        if not os.path.exists(file_path):
            raise FileNotFoundError('Import file not found')

        Source.__validate_source_file_type(file_path)

        with open(file_path, 'r+') as csv_file:
            return list(csv.reader(csv_file))

    def aws(self)->list[tuple]:
        print('Importing from aws...')
        filename = Config.get_s3_filename()
        if not filename:
            print('Aws filename not provided. Did you forget to set it in config module?')

        content = Aws().get(filename).decode('utf-8')
        Source.__validate_source_file_type(content, content_type='buffer')

        return list(csv.reader(content.splitlines()))

    @staticmethod
    def __validate_source_file_type(content, content_type='path'):
        m = magic.Magic(mime=True)
        mime = m.from_buffer(content) if content_type == 'buffer' else m.from_file(content)

        if not mime in [
            'text/csv',
            'text/plain',
            'application/vnd.ms-excel',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        ]:
            raise ValueError('Import file type not supported')