from typing import Union, Optional

from fastapi import Depends

from fastapi_identity.authorization.authorization_provider import AuthorizationProvider
from fastapi_identity.authorization.exc import AuthorizationError
from fastapi_identity.authorization.handler_context import AuthorizationHandlerContext
from fastapi_identity.authorization.policy_builder import AuthorizationPolicyBuilder
from fastapi_identity.builders.depends import depends
from fastapi_identity.exc import InvalidOperationException

__all__ = ("authorize",)

from fastapi_identity.signin_manager import SignInManager


async def _check_roles(
        roles: Union[set[str], str],
        context: AuthorizationHandlerContext
):
    if context.user is None:
        raise AuthorizationError()

    if isinstance(roles, str):
        roles = set(roles.replace(' ', '').split(','))

    result = any([context.user.is_in_role(r) for r in roles])

    if not result:
        raise AuthorizationError()


async def _check_policy(
        policy: str,
        context: AuthorizationHandlerContext,
        provider: AuthorizationProvider
):
    _policy = provider.get_policy(policy)

    if _policy is None:
        raise InvalidOperationException()

    for req in _policy.requirements:
        await req.handle(context)

    if not context.has_succeeded:
        raise AuthorizationError()


def authorize(
        *,
        roles: Optional[Union[set[str], str]] = None,
        policy: Optional[str] = None
):
    """

    :param roles:
    :param policy: 
    :return:
    """
    async def wrapped(
            context: AuthorizationHandlerContext = Depends(),
            provider: AuthorizationProvider = Depends(),
            manager: SignInManager = Depends(depends.SignInManager)
    ):
        if await manager.validate_security_stamp(context.user) is None:
            raise AuthorizationError()

        if roles:
            await _check_roles(roles, context)

        if policy:
            await _check_policy(policy, context, provider)

    return wrapped
