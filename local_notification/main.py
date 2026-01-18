import tkinter as tk
from tkinter import messagebox
import datetime
import sys
from config import configs

initials = []

def display_pop_up(root):
    if not initials:
        for config in configs:
            initials.append(config['initial'])

    while True:
        if not initials:
            sys.stderr.write('Initials not set, terminating...')

        now = datetime.datetime.now()

        for i, config in enumerate(configs):
            validate(i, config)

            if now - initials[i] >= datetime.timedelta(seconds=config['timeout']):
                messagebox.showwarning(title=config['messages']['title'], message=config['messages']['message'])
                root.withdraw()
                initials[i] = datetime.datetime.now()

def validate(index: int, config: dict):
    if not initials[index]:
        sys.stderr.write('Initial time not set, terminating...')

    if not config['messages'] or not config['messages']['title'] or not config['messages']['message']:
        sys.stderr.write('Messages not set or malformed, terminating...')

    if not config['timeout']:
        sys.stderr.write('Timeout not set, terminating...')

def main():
    root = tk.Tk()
    root.geometry('1x1')

    display_pop_up(root)

    root.mainloop()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.stdout.write('Terminating...')