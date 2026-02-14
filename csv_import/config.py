
class Config:
    @staticmethod
    def get_title_line()->list[str]:
        return [
            'first_name',
            'last_name',
            'email',
            'dob',
        ]

    @staticmethod
    def get_s3_filename():
        filename = 'test_import.csv'

    #
    # local or aws
    #
    @staticmethod
    def get_csv_source():
        return 'aws'