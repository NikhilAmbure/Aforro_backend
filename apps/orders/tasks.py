from celery import shared_task

from .models import Order


@shared_task
def send_order_confirmation(order_id):
    order = Order.objects.get(id=order_id)

    print(
        f"Order #{order.id} has been confirmed."
    )

    return True