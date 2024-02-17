import dataclasses
from abc import abstractmethod
from datetime import timedelta
from typing import Callable, cast, TYPE_CHECKING

from fastapi import Request, Response
from fastapi.security.base import SecurityBase
from starlette.authentication import AuthenticationError

from fastapi_identity.claims import ClaimsPrincipal

if TYPE_CHECKING:
    from fastapi_identity.http_context import HttpContext


@dataclasses.dataclass
class TokenValidationParameters:
    verify_signature: bool = True
    verify_aud: bool = True
    verify_iat: bool = True
    verify_exp: bool = True
    verify_nbf: bool = True
    verify_iss: bool = True
    verify_sub: bool = True
    verify_jti: bool = True
    verify_at_hash: bool = True
    require_aud: bool = True
    require_iat: bool = False
    require_exp: bool = True
    require_nbf: bool = False
    require_iss: bool = True
    require_sub: bool = False
    require_jti: bool = False
    require_at_hash: bool = False
    leeway: int = 60


@dataclasses.dataclass
class TokenAuthenticationOptions:
    audience: str = "@LOCALHOST AUTHORITY"
    issuer: str = "@LOCALHOST AUTHORITY"
    expires: timedelta = timedelta(minutes=15)


class AuthenticationBackend:
    def __init__(
            self,
            scheme: SecurityBase,
            secret: str
    ):
        self.scheme = cast(Callable, scheme)
        self._secret = secret

    async def authenticate(self, request: Request) -> ClaimsPrincipal:
        token: str = await self.scheme(request)
        if not token:
            raise AuthenticationError()
        return await self._authenticate(request, token)

    @abstractmethod
    async def _authenticate(self, request: Request, token: str) -> ClaimsPrincipal:
        pass

    @abstractmethod
    async def sign_in(self, context: 'HttpContext', user: ClaimsPrincipal) -> Response:
        pass

    @abstractmethod
    async def sign_out(self, context: 'HttpContext') -> None:
        pass
