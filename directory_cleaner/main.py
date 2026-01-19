import os
import sys
import directories

def main():
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