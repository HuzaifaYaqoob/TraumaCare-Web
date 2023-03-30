

from django.core.mail import send_mail, EmailMultiAlternatives

from django.template.loader import get_template

from django.conf import settings

def sendOtpEmail(data):
    """
    In context
        user and verification_code keys are required and there instances in values
    """
    
    user = data.get('user', None)
    
    #     Sending Dummy Email
    send_mail(
        'Verification Code',
        'Here is the message.',
        settings.EMAIL_HOST_USER,
        [settings.EMAIL_HOST_USER, user.email],
        fail_silently=False,
    )
    
    
    
    verification_code = data.get('verification_code', None)
    if not user or not verification_code:
        return
    
    context = data
    

    html_file = get_template('Email/otp_email.html')
    html_content = html_file.render(context)
    text_content = 'This is an important message.'

    msg = EmailMultiAlternatives(
        'Verification Code', 
        text_content,
        settings.EMAIL_HOST_USER,
        [user.email],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


    
