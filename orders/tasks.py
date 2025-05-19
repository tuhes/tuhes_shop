from django.conf import settings
from django.core.mail import EmailMessage
from orders.models import Order
from django.core.mail import send_mail
from celery import shared_task
from orders.pdf import generate_order_pdf


@shared_task
def sent_email_after_order_created(order_id):
    order = Order.objects.get(id=order_id)
    subject = f'Заказ №{order_id} от {order.created_at.strftime("%d.%m.%Y %H:%M")}'
    message = (f'{order.user.username},\n'
               f'Ваш заказ №{order_id} успешно оформлен!\n'
               f'На сумму {order.get_total_cost()}\n'
               f'Скидка составила: {order.get_discount()}\n'
               f'Итого к оплате: {order.get_total_cost_with_discount()}')
    mail_sent = send_mail(subject, message, settings.EMAIL_HOST_USER, [order.email])
    return mail_sent

@shared_task
def sent_email_after_order_created_with_attachment(order_id):
    order = Order.objects.get(id=order_id)
    pdf_file = generate_order_pdf(order)
    email = EmailMessage(
        subject=f'Заказ №{order_id} от {order.created_at.strftime("%d.%m.%Y %H:%M")}',
        body=f'{order.user.username},\nВаш заказ №{order_id} успешно оформлен!\nНа сумму {order.get_total_cost()} руб.\nСкидка составила: {order.get_discount()} руб.\nИтого к оплате: {order.get_total_cost_with_discount()} руб.',
        from_email=settings.EMAIL_HOST_USER,
        to=[order.email]
    )
    email.attach(filename=f'order_{order_id}_{order.created_at.strftime("%d_%m_%Y_%H_%M")}.pdf',
                 content=pdf_file.getvalue(),
                 mimetype='application/pdf')
    email.send()