import abc
import datetime
import os
import random
import boto3
from pydrive4.drive import GoogleDrive


class AbstractFactory(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def get(cls):
        pass

class AwsClientFactory(AbstractFactory):
    __client = None

    @classmethod
    def get(cls):
        if cls.__client:
            return cls.__client

        client = boto3.client(
            's3',
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
            region_name=os.environ.get("AWS_REGION")
        )

        cls.__client = client

        return client

class Aws:
    def __init__(self):
        self.__client = AwsClientFactory.get()
        self.__bucket = os.environ.get("AWS_S3_BUCKET")

    def get(self, filename: str)->bytes:
        result = self.__client.get_object(
            Bucket=self.__bucket,
            Key=filename
        )

        return result['Body'].read()

class GoogleDriveClientFactory(AbstractFactory):
    __client = None

    @classmethod
    def get(cls):
        if cls.__client:
            return cls.__client

        client = GoogleDrive(
            credentials_name=os.environ.get("GOOGLE_SERVICE_ACCOUNT"),
            service_account=True
        )

        cls.__client = client

        return client

class Drive:
    def __init__(self):
        self.__client: GoogleDrive = GoogleDriveClientFactory.get()

    def get(self, file_id: str)->str:
        local_filename = f'{int(datetime.datetime.now().timestamp())}_{random.randint(0, 999999)}.csv'
        local_filepath = os.path.join('temp', local_filename)

        result = self.__client.download_file(file_id=file_id, output_path=local_filepath)

        if result['success']:
            return result['path']

        raise FileNotFoundError('Could not download file')