from dependency_injector import containers, providers

from orders.domain.services.orders import OrderService
from orders.external.postgres.repositories.orders import OrderRepo


class OrdersRepositoryContainer(containers.DeclarativeContainer):
    orders_repo = providers.Factory(OrderRepo)
    products_snapshot_repo = providers.Factory()


class OrderServiceContainer(containers.DeclarativeContainer):
    order_service = providers.Factory(
        OrderService,
        order_repo=OrdersRepositoryContainer.orders_repo,
        product_snapshot_repo=OrdersRepositoryContainer.products_snapshot_repo,
    )
