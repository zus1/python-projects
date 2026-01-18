import datetime

configs = [
    {
        'messages': {
            'title': 'Touch grass',
            'message': 'Get up and touch some grass',
        },
        'timeout': 10,
        'initial': datetime.datetime.now(),
    },
    {
        'messages': {
            'title': 'Drink water',
            'message': 'Get up and drink some water',
        },
        'timeout': 20,
        'initial': datetime.datetime.now(),
    },
    {
        'messages': {
            'title': 'Take a walk',
            'message': 'go out and take a walk',
        },
        'timeout': 30,
        'initial': datetime.datetime.now(),
    },
]