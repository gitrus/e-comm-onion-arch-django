from django.http import HttpRequest
from ninja import Router

from e_comm_onion_arch.api_auth import AuthBearer
from orders.containers import OrderServiceContainer
from orders.domain.entities.service_requests import CreateOrderRequest
from orders.domain.services.orders import OrderService
from orders.view.schemes.orders import OrderScm

router = Router()


@router.post("/", auth=AuthBearer(), response=OrderScm)
def add(request: HttpRequest, order_req: CreateOrderRequest) -> OrderScm:
    o_s: OrderService = OrderServiceContainer.order_service()
    user_uid = request.auth.user_uid  # type: ignore # TODO: fixx type
    order = o_s.create_order(
        CreateOrderRequest(
            user_id=user_uid,
            shipping_address=order_req.shipping_address,
            order_items=order_req.order_items,
        )
    )

    return OrderScm.model_validate(order, from_attributes=True)
