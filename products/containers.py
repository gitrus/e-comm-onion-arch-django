from dependency_injector import containers, providers

from products.domain.services.products import ProductService


class ProductRepositoryContainer(containers.DeclarativeContainer):
    products_repo = providers.Factory()
    products_snapshot_repo = providers.Factory()


class ProductServiceContainer(containers.DeclarativeContainer):
    product_service = providers.Factory(
        ProductService,
        products_repo=ProductRepositoryContainer.products_repo,
    )
