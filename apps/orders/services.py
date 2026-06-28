from django.db import transaction
from django.db.models import F

from .models import Order, OrderItem
from apps.stores.models import Store, Inventory


@transaction.atomic
def create_order(validated_data):
    store = validated_data["store"]
    items = validated_data["items"]

    inventory_records = {}
    stock_available = True

    # Validating inventory
    for item in items:
        product = item["product"]
        quantity_requested = item["quantity_requested"]

        try: 
            # ---> This locks the inventory row while the transaction is running. --> select_for_update()
            inventory = Inventory.objects.select_for_update().get( 
                store = store, 
                product = product
            )

            inventory_records[product] = inventory

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