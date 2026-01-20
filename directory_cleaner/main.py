import os
import sys
import datetime
import directories
import scheduled
import repeat_values
import time

cleaned_directories = []
rescheduled_directories = {}

def main():
    try:
        if scheduled.scheduled:
            while True:
                sys.stdout.write('Running scheduled directory cleanup\n')
                scheduled_clean_directories()
                time.sleep(60)
        clean_directories()
    except KeyboardInterrupt:
        sys.stdout.write('\nInterrupted! Terminating...\n')

def scheduled_clean_directories():
    for directory in directories.get_directories():
        if directory['name'] in cleaned_directories:
            continue
        if not os.path.exists(directory['name']):
            sys.stderr.write(f'Directory: {directory['name']} does not exist\n')
            continue

        if not 'schedule' in directory.keys():
            clean_directory(directory['name'], rm=directory['rm'])
            cleaned_directories.append(directory['name'])
            continue

        scheduled_str = directory['schedule'] if not directory['name'] in rescheduled_directories.keys() \
            else rescheduled_directories[directory['name']]

        scheduled_datetime = get_scheduled_datetime(scheduled_str)

        if scheduled_datetime <= datetime.datetime.now().astimezone(datetime.timezone.utc):
            clean_directory(directory['name'], rm=directory['rm'])

            if directory['rm']:
                cleaned_directories.append(directory['name'])
                continue

            if 'repeat' in directory.keys() and 'repeat_every' in directory.keys():
                rescheduled_datetime = reschedule(scheduled_datetime, repeat_in=directory['repeat_every'])
                rescheduled_directories[directory['name']] = rescheduled_datetime.isoformat()
            else:
                cleaned_directories.append(directory['name'])


def reschedule(scheduled_datetime: datetime.datetime, repeat_in: str):
    repeat_period, unit = repeat_in.split(' ')

    if unit == repeat_values.MINUTES:
        scheduled_datetime = scheduled_datetime + datetime.timedelta(minutes=int(repeat_period))
    if unit == repeat_values.HOURS:
        scheduled_datetime = scheduled_datetime + datetime.timedelta(hours=int(repeat_period))

    return scheduled_datetime


def get_scheduled_datetime(scheduled_datetime: str) -> datetime.datetime | None:
    try:
        dt = datetime.datetime.fromisoformat(scheduled_datetime).replace(tzinfo=datetime.timezone.utc)
    except Exception as e:
        sys.stderr.write(f'Could not parse scheduled date: {str(e)}\n')
        return None

    return dt

def clean_directories():
    for directory in directories.get_directories():
        if not os.path.exists(directory['name']):
            sys.stderr.write(f'Directory: {directory['name']} does not exist\n')
            continue

        clean_directory(directory['name'], rm=directory['rm'])

def clean_directory(directory: str, rm: bool = False) -> None:
    files = os.listdir(directory)
    for file in files:
        full_path = os.path.join(directory, file)
        if os.path.isdir(full_path):
            clean_directory(full_path, rm=True)

            continue

        os.remove(full_path)

        if os.path.exists(full_path):
            sys.stderr.write(f'Could not delete file: {full_path}\n')
        else:
            sys.stdout.write(f'File successfully deleted: {full_path}\n')

    if len(os.listdir(directory)) != 0 and rm:
        sys.stderr.write(f'Could not delete directory {directory}. Not empty!\n')

    if rm:
        os.rmdir(directory)
        sys.stdout.write(f'Directory successfully deleted: {directory}\n')

if __name__ == '__main__':
    main()