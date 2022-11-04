import mailchimp_transactional as MailchimpTransactional
from mailchimp_transactional.api_client import ApiClientError

MAILCHIMP_API_KEY = 'YRxKQk091G8qZlp9FjIxtw'

try:
    mailchimp = MailchimpTransactional.Client(MAILCHIMP_API_KEY)
    response = mailchimp.users.ping()
    print('API called successfully: {}'.format(response))
except ApiClientError as error:
    print('An exception occurred: {}'.format(error.text))

mailchimp = MailchimpTransactional.Client(MAILCHIMP_API_KEY)

message = {
    "from_email": "giftlist@priesters.com",
    "from_name": "Matt Clarke",
    "subject": "testing python script",
    "text": "ROC/AUC = 0.91",
    "to": [
      {
        "email": "mphillips@multivaluecentral.com",
        "type": "to"
      }
    ]
}

try:
    mailchimp = MailchimpTransactional.Client(MAILCHIMP_API_KEY)
    response = mailchimp.messages.send({"message": message})
    print('API called successfully: {}'.format(response))
except ApiClientError as error:
    print('An exception occurred: {}'.format(error.text))

