import boto3
from datetime import datetime

from mypy_boto3_ses import SESClient

ses_client: SESClient = boto3.client(
    "ses",
    endpoint_url="http://127.0.0.1:4566"
)

body_text = 'This is a test email sent from AWS SES using Boto3.'
body_html = '<html><body><h1>This is a test email sent from AWS SES using Boto3.</h1></body></html>'

response = ses_client.send_email(
    Source="hello@example.com",
    Destination={"ToAddresses": ['recipient@example.com']},
    Message={
        'Subject': {'Data': 'Test Email from AWS SES'},
        'Body': {
            'Text': {'Data': body_text},
            'Html': {'Data': body_html}
        }
    }
)
print(response)
