## About
This application will send desired messages to each email from the list.

## How to run

Open terminal

Create and activate virtual environment

```
python -m venv .venv
source .venv/bin/activate
```

Install required libraries (only dotenv is required)

```
pip install -m requirements.txt
```

Copy .env.dist to .env file and add your credentials
```
cp .env.dist .env
```

Run main.py

```
python main.py
```

## Instructions
Add recipients in messages.py. If you wish to send a custom message to one or more recipients, add them to messages.py get_messages().
If custom message is added, it will be sent instead of default one, for that recipient. Default message is sent to all recipients without override

It is possible to load emails from file. Supported are csv and json (see example files).
If files with emails exist, then those files will be used as source of messages and recipients instead of messages.py.
Priority is csv >> json

Google SMTP server is used by default.

Google SMTP server requires app password, read more here https://support.google.com/accounts/answer/185833?hl=en