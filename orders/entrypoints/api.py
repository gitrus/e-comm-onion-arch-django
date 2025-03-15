from functools import partial

from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI, Swagger

from e_comm_onion_arch.api_auth import on_invalid_token
from e_comm_onion_arch.api_exceptions import InvalidToken
from orders.view.v1 import orders_router

api = NinjaAPI(docs=Swagger())

api.exception_handler(InvalidToken)(partial(on_invalid_token, api))

api.add_router("/v1/orders", orders_router)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
