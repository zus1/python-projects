import random
import hmac
import hashlib


class Generator:
    def __init__(self):
        self.__numbers = '0123456789'
        self.__symbols = '!@#$%^&*()'
        self.__letters = 'abcdefghijklmnoprstuvzwyx'
        self.__upper_case_letters = self.__letters.upper()
        self.__default_length = 8

        self.__upper_case_required = False
        self.__numbers_required = False
        self.__symbols_required = False
        self.__encode = False
        self.__encoding_key = ''

    @property
    def upper_case_required(self)->bool:
        return self.__upper_case_required
    @upper_case_required.setter
    def upper_case_required(self, upper_case_required: bool):
        self.__upper_case_required = upper_case_required

    @property
    def numbers_required(self)->bool:
        return self.__numbers_required
    @numbers_required.setter
    def numbers_required(self, numbers_required: bool):
        self.__numbers_required = numbers_required

    @property
    def symbols_required(self)->bool:
        return self.__symbols_required
    @symbols_required.setter
    def symbols_required(self, symbols_required: bool):
        self.__symbols_required = symbols_required

    @property
    def encode(self)->bool:
        return self.__encode
    @encode.setter
    def encode(self, encode: bool):
        self.__encode = encode

    @property
    def encoding_key(self)->str:
        return self.__encoding_key
    @encoding_key.setter
    def encoding_key(self, encoding_key: str):
        self.__encoding_key = encoding_key

    def generate(self, length: int|None = None):
        length = length if length else self.__default_length

        # if not self.__upper_case_required and not self.__numbers_required and not self.__symbols_required:
        #     return self.__generate_random_password(length=length)

        password = ''
        if self.__upper_case_required:
            length = length - 1
            password += random.choice(self.__upper_case_letters)
        if self.__numbers_required:
            length = length - 1
            password += random.choice(self.__numbers)
        if self.__symbols_required:
            length = length - 1
            password += random.choice(self.__symbols)

        if length < 0:
            raise ValueError('Required password length is to short and do not allow to include desired complexity')

        if length == 0:
            return password

        password = self.__generate_random_password(length=length, prefix=password)

        shuffled = Generator.__shuffle_password(password)

        if self.__encode:
            return self.__encode_password(shuffled)

        return shuffled

    def __encode_password(self, plain_password)->str:
        if not self.__encoding_key:
            raise ValueError('Encryption key not provided')

        return hmac.new(
            key=self.encoding_key.encode('ascii'),
            msg=plain_password.encode('ascii'),
            digestmod=hashlib.sha256
        ).hexdigest()

    @staticmethod
    def __shuffle_password(password: str)->str:
        l = list(password)
        random.shuffle(l)

        return ''.join(l)

    def __generate_random_password(self, length: int, prefix: str | None = None)->str:
        pool = self.__letters + self.__numbers + self.__symbols + self.__upper_case_letters

        password = prefix if prefix else ''
        for _ in range(length):
            password += random.choice(pool)
        return password


