import sys
import smtplib, ssl
import os
import messages
import csv
import json
from dotenv import load_dotenv

def main():
    load_dotenv()

    context = ssl.create_default_context()
    port = os.environ.get('SSL_PORT', 465)
    smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
    sender_email = os.environ.get('SENDER', '')
    app_password = os.environ.get('APP_PASSWORD', '')

    if not sender_email or not app_password:
        raise RuntimeError('Please set your email address and app password.')

    with smtplib.SMTP_SSL(host=smtp_server, port=port, context=context) as server:
        try:
            server.login(sender_email, app_password)
        except smtplib.SMTPAuthenticationError as ex:
            raise RuntimeError(str(ex))

        texts, recipients = get_messages()

        for recipient in recipients:
            text = get_message(texts, recipient)

            try:
                server.sendmail(sender_email, recipient, text)
            except Exception as ex:
                sys.stdout.write(f'Could not send message to {recipient}: {str(ex)}\n')
                return

            sys.stdout.write(f'Message sent to recipient {recipient}\n')

def get_messages()->tuple[dict[str, str], list[str]]:
    default_texts = messages.get_messages()

    #First try to get recipients and custom messages from csv file
    if os.path.exists('./emails.csv'):
        with open('./emails.csv', 'r') as csvfile:
            csv_reader = list(csv.reader(csvfile, delimiter=','))

            texts = {
                'default' : default_texts['default'],
            }
            recipients = []
            for row in csv_reader:
                recipients.append(row[0])
                if len(row) == 2:
                    texts[row[0]] = row[1]

            return texts, recipients

    #If no csv file, try to get the same from JSON file
    if os.path.exists('./emails.json'):
        with open('./emails.json', 'r') as jsonfile:
            json_dict = json.load(jsonfile)
            texts = {key : value for key, value in json_dict.items() if value}
            texts['default'] = default_texts['default']
            recipients = [key for key in json_dict.keys()]

            return texts, recipients

    #If no custom files use ones set in messages.py
    return default_texts, messages.get_recipients()

def get_message(texts: dict, recipient: str)->str:
    if recipient in texts.keys():
        return texts[recipient]

    return texts['default']

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.stdout.write('Terminating...')
    except RuntimeError as e:
        sys.stdout.write(str(e) + '\n')