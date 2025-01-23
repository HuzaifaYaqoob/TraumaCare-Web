

from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings


def sendNewOrderEmailToAdmin(order_instance, email_log_instance=None):
    order_items = []
    for itm in order_instance.order_items.all():
        order_items.append(f'\t{itm.product.name} \t\t {itm.final_price}x{itm.quantity}')
    
    subject = 'TraumaCare : New Order'
    message = f"""
            New Order.\n
            Order ID : #{order_instance.id}\n
            Date : #{str(order_instance.created_at)}\n
            User : {order_instance.user.full_name}\n
            subtotal : {order_instance.subtotal}\n
            discount : {order_instance.discount}\n
            platform_fee : {order_instance.platform_fee}\n
            delivery_charges : {order_instance.delivery_charges}\n
            total_amount : {order_instance.total_amount}\n
            Order Items : {order_instance.order_items.all().count()}\n
            {"\n".join(order_items)}\n
        """
    recievers = [settings.EMAIL_HOST_USER, 'huzaifa.officialmail@gmail.com']

    if email_log_instance:
        email_log_instance.emails = ', '.join(recievers)
        email_log_instance.subject = subject
        email_log_instance.message = message
        email_log_instance.save()

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        recievers,
        fail_silently=False,
    )

    if email_log_instance:
        email_log_instance.is_sent = True
        email_log_instance.save()
    