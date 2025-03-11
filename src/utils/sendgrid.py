import requests
import sendgrid
from faker import Faker

fake = Faker()


class SendGrid:
    def __init__(self, api_key: str):
        self.client = sendgrid.SendGridAPIClient(api_key=api_key)
        self.api_key = api_key
        self.from_email = 'abc@minabank.net'

    def send_random_mail(self, to_email: str):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
        }
        # url = f"https://api.sendgrid.com/v3/messages?query=to_email='{to_email}'"
        url = 'https://api.sendgrid.com/v3/mail/send'
        subject = fake.sentence(nb_words=10)
        content = fake.paragraph(nb_sentences=10)
        data = {
            'personalizations': [{'to': [{'email': to_email}], 'subject': subject}],
            'from': {'email': self.from_email},
            'content': [{'type': 'text/html', 'value': content}],
        }
        try:
            response = requests.post(url, json=data, headers=headers)
            print(f'Response Code: {response.status_code}')
            print(f'Response Body: {response.json()}')
        except Exception as e:
            print(f'Error sending email: {e}')
        return subject
