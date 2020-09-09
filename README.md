# http-up-check
Checks that an HTTP endpoint returns a non 5xx status. \
This script is intended for checking that a service is up, not for testing that a service is working correctly.
The script is designed to be run as a cron job, and will email you when it has run.

## Prerequisites
- Access to an SMTP mail server
- Python 3.x
- Installed libraries from `requirements.txt`

## Usage
```shell
python3 main.py [flags]
```

## Flags
- `-u` | `--url` REQUIRED URL to test 
- `-e` | `--emails` REQUIRED Comma separated list of emails to notify
- `-a` | `--notify-always` When present, will send an email even if test was successful

## Required envioroment variables
SMTP connection and login details:
- `EMAIL_HOST`
- `EMAIL_PORT`
- `EMAIL_HOST_USER`
- `EMAIL_HOST_PASSWORD`
