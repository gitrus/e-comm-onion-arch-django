from dependency_injector import containers, providers

from orders.external.products.product_client import ProductClient


class ProductClientContainer(containers.DeclarativeContainer):
    product_service_container = providers.DependenciesContainer()
    client = providers.Factory(
        ProductClient,
        product_service=product_service_container.product_service,
    )
