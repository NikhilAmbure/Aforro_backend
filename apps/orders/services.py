from .tasks import send_order_confirmation
from django.db import transaction
from django.db.models import F

from .models import Order, OrderItem
from apps.stores.models import Store, Inventory


@transaction.atomic
def create_order(validated_data):
    store = validated_data["store"]
    items = validated_data["items"]

    stock_available = True

    # Validating inventory
    for item in items:
        product = item["product"]
        quantity_requested = item["quantity_requested"]

        try: 
            
            inventory = Inventory.objects.select_for_update().get( 
                store = store, 
                product = product
            )

            if inventory.quantity < quantity_requested:
                stock_available = False 

        except Inventory.DoesNotExist:
            stock_available = False
        
    # Create the order
    order = Order.objects.create(
        store=store,
        status=(
            Order.StatusChoices.CONFIRMED
            if stock_available
            else Order.StatusChoices.REJECTED
        ),
    )

    if stock_available:
        transaction.on_commit(
            lambda: send_order_confirmation.delay(order.id)
        )

    # Create OrderItems and deduct stock if confirmed
    for item in items:
        product = item["product"]
        quantity_requested = item["quantity_requested"]

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity_requested=quantity_requested,
        )

        if stock_available:
            Inventory.objects.filter(
                store=store,
                product=product,
            ).update(
                quantity = F("quantity") - quantity_requested
            )
        
    return order