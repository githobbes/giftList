import base64
from pathlib import Path
import mailchimp_transactional as MailchimpTransactional
from mailchimp_transactional.api_client import ApiClientError as ApiClientError_Trans
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError as ApiClientError_Mark

MAILCHIMP_API_KEY = 'YRxKQk091G8qZlp9FjIxtw'

PATH_TO_TEMPLATES = (Path.home() / "PycharmProjects" / "giftlist" / "data")

# Add contact to audience list (need to check if they're already in the list, but yeah)
mailchimp = MailchimpMarketing.Client()
mailchimp.set_config({
  "api_key": MAILCHIMP_API_KEY,
  "server": "us12"
})

body = {
  "permission_reminder": "You provided e-mail addresses for contact purposes.",
  "email_type_option": False,
  "campaign_defaults": {
    "from_name": "Priester's Pecans",
    "from_email": "giftlist@priesters.com",
    "subject": "Holiday Gift List",
    "language": "EN_US"
  },
  "name": "Corporate Gift List",
  "contact": {
    "company": "Priester's Pecans",
    "address1": "208 Old Fort Road East",
    "address2": "",
    "city": "Fort Deposit",
    "state": "AL",
    "zip": "36032",
    "country": "US"
  }
}

# Adding Audience member to "Priester's Pecans, Inc."
list_id = "6564a41a89"

# Adding Corporate Gift List Audience...?
try:
    response = mailchimp.lists.create_list(body)
    print("Response: {}".format(response))
except ApiClientError_Mark as error:
    print("An exception occurred: {}".format(error.text))

# Collecting attachment file
attachment_name = f"buyer_page.pdf"
attachment_path = (PATH_TO_TEMPLATES / attachment_name)
with open(str(attachment_path), "rb") as pdf_file:
    attachment_content = base64.b64encode(pdf_file.read()).decode('utf-8')

message = {
    "from_email": "giftlist@priesters.com",
    "from_name": "Priester's Pecans",
    "subject": "Gift List Order Form",
    "to": [
        {
            "email": "phillimj@mail.gvsu.edu",
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
            "name": "Gift List Order Form.pdf",
            "content": attachment_content
        }
    ]
}

try:
    mailchimp = MailchimpTransactional.Client(MAILCHIMP_API_KEY)
    response = mailchimp.messages.send_template({"template_name": "Gift List Corporate 2022",
                                                 "template_content": [{}],
                                                 "message": message})
    print('API called successfully: {}'.format(response))
except ApiClientError_Trans as error:
    print('An exception occurred: {}'.format(error.text))
