from datetime import timedelta, datetime, UTC
from typing import Callable, TYPE_CHECKING

from fastapi import Request, Response
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from starlette.authentication import AuthenticationError
from starlette.responses import JSONResponse

from fastapi_identity.authentication.base import AuthenticationBackend, TokenValidationParameters
from fastapi_identity.claims import ClaimsPrincipal, ClaimTypes, Claim
from fastapi_identity.utils import asdict

if TYPE_CHECKING:
    from fastapi_identity.http_context import HttpContext


class BearerAuthenticationBackend(AuthenticationBackend):
    def __init__(
            self,
            secret: str,
            tokenUrl: str,
            expires: timedelta = timedelta(minutes=5),
            *,
            configure_validation_parameters: Callable[[TokenValidationParameters], None] = None,
            valid_audience: str = "@LOCALHOST AUTHORITY",
            valid_issuer: str = "@LOCALHOST AUTHORITY"
    ):
        super().__init__(OAuth2PasswordBearer(tokenUrl=tokenUrl, auto_error=False), secret)
        self.expires = expires
        self.valid_audience = valid_audience
        self.valid_issuer = valid_issuer
        self.__token_validation_parameters = TokenValidationParameters()

        if configure_validation_parameters is not None:
            configure_validation_parameters(self.__token_validation_parameters)

    async def _authenticate(self, request: Request, token: str) -> ClaimsPrincipal:
        try:
            payload = jwt.decode(
                token,
                self._secret,
                algorithms='HS256',
                options=asdict(self.__token_validation_parameters),
                audience=self.valid_audience,
                issuer=self.valid_issuer
            )
        except JWTError:
            raise AuthenticationError()

        principal = ClaimsPrincipal(
            *[Claim.load(claim) for claim in payload.get('claims')],
            *[Claim.load(claim) for claim in payload.get('roles')]
        )

        return principal

    async def sign_in(self, context: 'HttpContext', user: ClaimsPrincipal) -> Response:
        expires = datetime.now(UTC) + self.expires
        roles, other_claims = user.dump()
        data = {
            'exp': expires,
            'aud': self.valid_audience,
            'iss': self.valid_issuer,
            'sub': user.find_first_value(ClaimTypes.NameIdentifier),
            'roles': roles,
            'claims': other_claims
        }
        token = jwt.encode(data, self._secret)
        context.response = JSONResponse({'access_token': token, 'token_type': 'bearer'})
        return context.response

    async def sign_out(self, context: 'HttpContext') -> None:
        pass
