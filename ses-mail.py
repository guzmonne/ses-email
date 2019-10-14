import os
import sys
import time
import random
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart


import boto3
import lorem

TO = os.environ.get('TO')
CLIENT = None
HOUR_RATE = 100
ATTACHMENT_RATIO = 0.5
AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

def set_variables():
    global TO
    global CLIENT
    global HOUR_RATE
    global ATTACHMENT_RATIO
    global AWS_ACCESS_KEY
    global AWS_SECRET_ACCESS_KEY
    if AWS_ACCESS_KEY is None:
        sys.exit('AWS_ACCESS_KEY is not defined')
    if AWS_SECRET_ACCESS_KEY is None:
        sys.exit('AWS_SECRET_ACCESS_KEY is not defined')
    if len(sys.argv) < 2:
        sys.exit('TO email is not defined')
    CLIENT = boto3.client('ses', 
        aws_access_key_id=AWS_ACCESS_KEY, 
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    TO = sys.argv[1]
    try:
        HOUR_RATE = int(sys.argv[2])
    except IndexError:
        pass
    try:
        ATTACHMENT_RATIO = int(sys.argv[3])
    except IndexError:
        pass

def send_email():
    global CLIENT
    response = CLIENT.send_email(
            Source='no-reply@mail.conatest.click',
            Destination={
                'ToAddresses': [TO]
            },
            Message={
                'Subject': {
                    'Data': '[ses-mail] mail de prueba]'
                },
                'Body': {
                    'Text': {
                        'Data': lorem.text()
                    }
                }
            }
        )

    print(f'Message {response["MessageId"]} sent!')

def send_email_with_attachment():
    global CLIENT
    message = MIMEMultipart()
    message['Subject'] = '[ses-email] mail de prueba con adjunto'
    message['From'] = 'no-reply@mail.conatest.click'
    message['To'] = TO
    # Message Body
    part = MIMEText(lorem.text())
    message.attach(part)
    # Attachment
    part = MIMEApplication(open('attachment.jpg', 'rb').read())
    part.add_header('Content-Disposition', 'attachment',
        filename='attachment.jpg')
    message.attach(part)
    # Send email
    response = CLIENT.send_raw_email(
        Source=message['From'],
        Destinations=[TO],
        RawMessage={
            'Data': message.as_string()
        }
    )
    print(f'Message {response["MessageId"]} sent!')

def send_email_periodically(period):
    global ATTACHMENT_RATIO
    if random.uniform(0, 1) < ATTACHMENT_RATIO: 
        send_email_with_attachment()
    else:
        send_email()
    time.sleep(period)
    send_email_periodically(period)

if __name__ == '__main__':
    set_variables()
    period = 60 / HOUR_RATE

    print(f'Sending emails every {period}s')
    print(f'\nPress Ctrl+c to stop\n')

    try:
        send_email_periodically(period)
    except KeyboardInterrupt:
        print('\nDone')



