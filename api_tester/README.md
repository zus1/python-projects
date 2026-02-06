## About
Python application for sending one or multiple requests to api endpoints.

## How to run
Open terminal and run main.py
```
pip install -r requirements.txt

python main.py
```

## Instructions
Add requests you wish to send to pool list of dictionaries in poll.py.
Adjust config.py variables to configure in which way request will be executed.

Possible configuration parameters are:
1. sync - id set to true requests are going to be executed synchronously one after another, else execution is going to be asynchronous
2. key - if not None, only one request with specified key will be taken from the pool
3. num_of_requests - to be taken into consideration, key must be None. If integer specified number of request will be taken from the pool. If tuple, requests from first key to second key will be taken
4. duplicate_times - to be taken into consideration, both key and num_of_requests must be None. Radom request will be taken from the pool and multiplied duplicate times, times. If key is not None, then specific request at that key in the pool, will be duplicated