
def get_directories():
    return [
        {
            'name': '/var/www/html/test_cleaning',
            'rm': False,
            #Following are settings dor scheduled cleaning. Used when scheduled.scheduled is set to True
            # 'schedule': '2026-01-20 00:59:00', #must be in UTC
            # 'repeat': True,
            # 'repeat_every': '1 minutes' # minutes or hours
        },
    ]