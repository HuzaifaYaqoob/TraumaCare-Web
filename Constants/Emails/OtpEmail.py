

from django.core.mail import send_mail, EmailMultiAlternatives

from django.template.loader import get_template

from django.conf import settings

def sendOtpEmail(data):
    context = {}

    html_file = get_template('Email/otp_email.html')
    html_content = html_file.render(context)
    text_content = 'This is an important message.'

    msg = EmailMultiAlternatives(
        'Verification Code', 
        text_content,
        settings.EMAIL_HOST_USER,
        [settings.EMAIL_HOST_USER],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


    # send_mail(
    #     'Verification Code',
    #     'Here is the message.',
    #     settings.EMAIL_HOST_USER,
    #     [settings.EMAIL_HOST_USER],
    #     fail_silently=False,
    # )