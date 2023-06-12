from django.core.mail import EmailMessage


def send_email(data):
    email = EmailMessage(
        subject=data['email_subject'],
        body=data['email_body'],
        from_email="from@example.com",
        to=[data.get('to_email')]
    )
    email.send()
