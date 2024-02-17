import dataclasses
import json
import uuid
from datetime import timedelta, datetime, UTC
from typing import Callable, Optional, Union, Literal, TYPE_CHECKING

from cryptography.fernet import Fernet
from fastapi import Request, Response
from fastapi.security import APIKeyCookie
from jose import jwt, JWTError
from starlette.authentication import AuthenticationError

from fastapi_identity.authentication.base import AuthenticationBackend, TokenValidationParameters
from fastapi_identity.claims import ClaimsPrincipal, ClaimTypes, Claim
from fastapi_identity.utils import asdict

if TYPE_CHECKING:
    from fastapi_identity.http_context import HttpContext


@dataclasses.dataclass
class CookieOptions:
    max_age: Optional[int] = None
    path: str = "/"
    domain: Optional[str] = None
    secure: bool = False
    httponly: bool = False
    samesite: Optional[Literal["lax", "strict", "none"]] = "lax"


class CookieAuthenticationBackend(AuthenticationBackend):
    def __init__(
            self,
            secret: str,
            name: str = ".fastapi.identity.auth",
            expires: timedelta = timedelta(days=7),
            *,
            configure_cookie_options: Callable[[CookieOptions], None] = None,
            configure_validation_parameters: Callable[[TokenValidationParameters], None] = None,
            valid_audience: str = "@LOCALHOST AUTHORITY",
            valid_issuer: str = "@LOCALHOST AUTHORITY",
            claim_cookie_prefix: str = ".fastapi.identity",
            encrypt_cookie_key: Optional[Union[bytes, str]] = None
    ):
        super().__init__(APIKeyCookie(name=name, auto_error=False), secret)
        self.name = name
        self.expires = expires
        self.valid_audience = valid_audience
        self.valid_issuer = valid_issuer
        self.__token_validation_parameters = TokenValidationParameters()
        self.cookie_options = CookieOptions()
        self.claim_cookie_prefix = claim_cookie_prefix + ".claim."
        self.fernet = Fernet(encrypt_cookie_key) if encrypt_cookie_key is not None else None

        if configure_cookie_options is not None:
            configure_cookie_options(self.cookie_options)

        if configure_validation_parameters is not None:
            configure_validation_parameters(self.__token_validation_parameters)

    async def _authenticate(self, request: Request, token: str) -> ClaimsPrincipal:
        try:
            jwt.decode(
                token,
                self._secret,
                algorithms='HS256',
                options=asdict(self.__token_validation_parameters),
                audience=self.valid_audience,
                issuer=self.valid_issuer
            )
        except JWTError:
            raise AuthenticationError()

        principal = ClaimsPrincipal()

        for cname, cvalue in request.cookies.items():
            if cname.startswith(self.claim_cookie_prefix):
                principal.add_claims(Claim.load(json.loads(self.decode_cookie(cvalue))))

        return principal

    async def sign_in(self, context: 'HttpContext', user: ClaimsPrincipal) -> Response:
        await self.sign_out(context)
        context.response.status_code = 200
        context.response.headers.append('Cache-Control', 'no-cache')
        expires = datetime.now(UTC) + self.expires
        data = {
            'exp': expires,
            'aud': self.valid_audience,
            'iss': self.valid_issuer,
            'sub': user.find_first_value(ClaimTypes.NameIdentifier)
        }
        token = jwt.encode(data, self._secret)
        context.response.set_cookie(self.name, token, expires=expires, **asdict(self.cookie_options))

        for claim in user.claims:
            context.response.set_cookie(
                key=self._generate_cookie_name(),
                value=self.encode_cookie(json.dumps(claim.dump())),
                expires=expires,
                **asdict(self.cookie_options)
            )

        return context.response

    async def sign_out(self, context: 'HttpContext') -> None:
        context.response.status_code = 200
        context.response.delete_cookie(self.name)
        self._remove_cookie_claims(context)

    def encode_cookie(self, value: Union[bytes, str]) -> str:
        if self.fernet is not None:
            if isinstance(value, str):
                value = value.encode()
            return self.fernet.encrypt(value).decode()
        return value

    def decode_cookie(self, data: Union[bytes, str]) -> str:
        if self.fernet is not None:
            return self.fernet.decrypt(data).decode()
        return data

    def _generate_cookie_name(self) -> str:
        return self.claim_cookie_prefix + str(uuid.uuid4())

    def _remove_cookie_claims(self, context: 'HttpContext'):
        for cname, cvalue in context.request.cookies.items():
            if cname.startswith(self.claim_cookie_prefix):
                context.response.delete_cookie(key=cname)
