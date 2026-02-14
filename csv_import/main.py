import dotenv
from database import Database
from sources import Source

def main():
    dotenv.load_dotenv()

    try:
        csv_lines = Source().read_from_source()
    except Exception as e:
        print(f'Error reading csv file. Error: {e}')

        return

    print('Importing, please wait...\n')
    Database().import_csv(csv_lines)
    print('Successfully imported\n')


if __name__ == '__main__':
    main()