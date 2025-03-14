from uuid import UUID

from django.http import HttpRequest, HttpResponse
from ninja import NinjaAPI
from ninja.security import HttpBearer
from pydantic import BaseModel

from e_comm_onion_arch.api_exceptions import InvalidToken


def on_invalid_token(api: NinjaAPI, request: HttpRequest, exc: Exception) -> HttpResponse:
    return api.create_response(request, {"detail": "Invalid token supplied"}, status=401)


class UserTokenScm(BaseModel):
    token: str
    user_uid: UUID


class AuthBearer(HttpBearer):
    def authenticate(self, request: HttpRequest, token: str) -> UserTokenScm:
        if token == "supersecret":  # noqa: S105 educational reason
            return UserTokenScm(
                token=token, user_uid=UUID("00000000-0000-0000-0000-000000000000")
            )
        raise InvalidToken
