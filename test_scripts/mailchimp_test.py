import base64
from pathlib import Path
import mailchimp_transactional as MailchimpTransactional
from mailchimp_transactional.api_client import ApiClientError

MAILCHIMP_API_KEY = 'YRxKQk091G8qZlp9FjIxtw'

PATH_TO_TEMPLATES = (Path.home() / "PycharmProjects" / "giftlist" / "data")

attachment_name = f"buyer_page.pdf"
attachment_path = (PATH_TO_TEMPLATES / attachment_name)
with open(str(attachment_path), "rb") as pdf_file:
    attachment_content = base64.b64encode(pdf_file.read()).decode('utf-8')

message = {
    "from_email": "giftlist@priesters.com",
    "from_name": "Priester's Pecans",
    "subject": "Gift List Order Form",
    "text": "Testing the Attachment API",
    "to": [
        {
            "email": "mphillips@multivaluecentral.com",
            "type": "to"

        },
        {
            "email": "mphillips@multivaluecentral.com",
            "type": "bcc"
        }
    ],
    "attachments": [
        {
            "type": 'application/pdf',
            "name": str(attachment_path),
            "content": attachment_content
        }
    ]
}

try:
    mailchimp = MailchimpTransactional.Client(MAILCHIMP_API_KEY)
    response = mailchimp.messages.send({"message": message})
    print('API called successfully: {}'.format(response))
except ApiClientError as error:
    print('An exception occurred: {}'.format(error.text))

