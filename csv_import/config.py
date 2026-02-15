
class Config:
    @staticmethod
    def get_title_line()->list[str]:
        return []

    @staticmethod
    def get_s3_filename():
        return 'test_import.csv'

    @staticmethod
    def get_drive_file_id():
        return '1vfA_A68FtdRu9bTEeSa-ooCbLoQahNMr'

    #
    # local|aws|drive
    #
    @staticmethod
    def get_csv_source():
        return 'local'