import os
import boto3

class ClientFactory:
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
        self.__client = ClientFactory.get()
        self.__bucket = os.environ.get("AWS_S3_BUCKET")

    def get(self, filename: str)->bytes:
        result = self.__client.get_object(
            Bucket=self.__bucket,
            Key=filename
        )

        return result['Body'].read()