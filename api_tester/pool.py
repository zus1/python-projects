import random

def validate_request(request: dict)->dict:
    if not 'method' in request.keys() or request['method'] == '':
        raise ValueError(f'Request method not defined. ID: {request.get("id") if "id" in request else ""}')
    if not 'base_url' in request.keys() or request['base_url'] == '':
        raise ValueError(f'Request base_url not defined. ID: {request.get("id") if "id" in request else ""}')
    if not 'path' in request.keys() or request['path'] == '':
        raise ValueError(f'Request path not defined. ID: {request.get("id") if "id" in request else ""}')

    return request


class Pool:
    def __init__(self):
        self.__pool = [
            {
                'id': 1, #internal id used for referencing, it's optional
                'method': 'GET',
                'base_url': 'https://example.com',
                'path': '/test/#p1#',
                'headers': {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                },
                'body': {
                    'body1': 'value1',
                    'body2': 'value2',
                },
                'params': {
                    'param1': 'value1',
                    'param2': 'value2',
                },
                'path_params': {
                    'p1': 'value1',
                },
                'options': {
                    'timeout': 10,
                }
            }
        ]


    def get_request(self, index: int):
        if len(self.__pool) - 1 > index:
            raise ValueError(f'Index {index} not found')
        if index < 0:
            raise ValueError('Index can not be negative')

        return [validate_request(self.__pool[index])]

    def take_from_pool(self, amount: int|tuple):
        if type(amount) == tuple:
            start = amount[0]
            stop = amount[1]

            if start < 0:
                raise ValueError('Start index can not be negative')
            if stop > len(self.__pool) - 1:
                raise ValueError('Stop exceeds amount of requests available in pool')

            if stop < start:
                raise ValueError('Stop index can not be smaller than start index')

            return [validate_request(request=request) for request in self.__pool[start:stop + 1]]

        if amount > len(self.__pool):
            raise ValueError('Requested amount exceeds amount of requests available in pool')
        if amount < 0:
            raise ValueError('Amount can not be negative')

        return [validate_request(request=request) for request in self.__pool[0:amount]]

    def duplicate_from_pool(self, times: int, key: int | None=None)->list:
        request = None
        if key is not None:
            request = self.__pool[key] if len(self.__pool) > key else None

        if request:
            validate_request(request=request)

            return [request for _ in range(times)]

        request = self.__pool[random.randint(0, len(self.__pool) - 1)]

        validate_request(request=request)

        return [request for _ in range(times)]