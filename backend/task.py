from workers import celery
from models import *
from mailer import send_email

@celery.task
def add():
    x = 1
    y = 2
    return x + y

@celery.task
def multiply(x, y):
    return x * y

@celery.task
def send_order_email(order_id):
    order = Order.query.get(order_id)
    body = f"Order Successful, Total Amount = {order.total_amount}"
    subject = "Order Successful"
    send_email(order.user_email, subject, body)
    return f"successfully sent email to {order.user.name}"