import time
from traceback import print_tb

import requests
import config
from concurrent.futures import ThreadPoolExecutor
from pool import Pool


def call_api(request: dict):
    content_type = find_content_type(request)

    start_time = time.time()
    response = requests.request(
        method=request.get('method'),
        url=construct_absolute_url(request),
        params=request.get('params') if 'params' in request else None,
        json=request.get('body') if content_type == 'application/json' else None,
        data=request.get('data') if content_type != 'application/json' else None,
        headers=request.get('headers') if 'headers' in request else None,
        **request.get('options') if 'options' in request else None
    )
    end_time = time.time()

    print({
        'request_id': request.get('id') if 'id' in request else None,
        'status_code': response.status_code,
        'text': response.text,
        'request_execution_time': end_time - start_time
    })

def find_content_type(request: dict)->str:
    if not 'headers' in request or not request['headers']:
        return 'application/json'

    headers = request.get('headers')

    if not 'Content-Type' in headers:
        return 'text/plain'

    return headers.get('Content-Type')

def construct_absolute_url(request: dict) -> str:
    url = trim(request['base_url'])
    path = trim(request['path'])

    if 'path_params' in request.keys() and request['path_params']:
        for path_param, param_value in request['path_params'].items():
            path = path.replace(f'#{path_param}#', param_value)

    return f'{url}/{path}'


def trim(url_part)->str:
    if url_part[-1] == '/':
        url_part = url_part[:len(url_part)-1]
    if url_part[0] == '/':
        url_part = url_part[1:]

    return url_part


def main():
    available_pool = Pool()

    try:
        if config.KEY is not None and config.DUPLICATE_TIMES is None:
            effective_pool = available_pool.get_request(config.KEY)
        elif config.NUM_OF_REQUESTS is not None:
            effective_pool = available_pool.take_from_pool(config.NUM_OF_REQUESTS)
        else:
            print('by duplicate')
            effective_pool = available_pool.duplicate_from_pool(times=config.DUPLICATE_TIMES, key=config.KEY)
    except ValueError as e:
        print(f'Could not take request from the pool. Error: {e}')

        return

    execution_started = time.time()

    if config.SYNC:
        execute_sync(effective_pool)
    else:
        execute_async(effective_pool)

    execution_ended = time.time()
    print(f'Total execution time: {execution_ended - execution_started}')


def execute_sync(eff_pool: list[dict]):
    for r in eff_pool:
        call_api(r)


def execute_async(eff_pool: list[dict]):
    with ThreadPoolExecutor(max_workers=len(eff_pool)) as executor:
        features = [executor.submit(call_api, r) for r in eff_pool]

        for sent_r, feature in zip(eff_pool, features):
            try:
                feature.result()
            except Exception as e:
                print(f'Could not execute request: {sent_r["id"] if "id" in sent_r else ""}. Error: {e}')


if __name__ == '__main__':
    main()