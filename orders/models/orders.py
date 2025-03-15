from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.db.models import JSONField

from e_comm_onion_arch.models_fixtures import enum_to_choices
from orders.domain.entities.value_objects import OrderStatus
from orders.models.product_snapshot import ProductSnapshot


class Order(models.Model):
    order_id = models.UUIDField(primary_key=True, editable=False)
    user_id = models.UUIDField()

    # related to entity.Address serialized to json
    shipping_address = JSONField(encoder=DjangoJSONEncoder)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(
        max_length=20,
        choices=enum_to_choices(OrderStatus),
        default=OrderStatus.PENDING.value,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OrderItem(models.Model):
    order_item_id = models.UUIDField(primary_key=True, editable=False)
    order = models.ForeignKey(Order, related_name="order_items", on_delete=models.CASCADE)
    product_snapshot = models.ForeignKey(ProductSnapshot, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
