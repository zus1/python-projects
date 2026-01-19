
def get_recipients()->list[str]:
    return [
        'zus.ozus@gmail.com',
        'mario.ozuska@gmail.com'
    ]

def get_messages()->dict[str, str]:
    return {
        'default': 'This general message will be sent to all recipients.',
        'zus.ozus@gmail.com': 'All the best wishes with your job hunting',
    }