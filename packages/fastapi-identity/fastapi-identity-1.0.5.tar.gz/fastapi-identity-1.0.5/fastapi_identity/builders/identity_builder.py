from typing import Iterable

from fastapi_identity.confirmation import IUserConfirmation
from fastapi_identity.error_describer import IdentityErrorDescriber
from fastapi_identity.options import TokenOptions
from fastapi_identity.password_validator import IPasswordValidator
from fastapi_identity.role_validator import IRoleValidator
from fastapi_identity.builders.depends import depends
from fastapi_identity.signin_manager import SignInManager
from fastapi_identity.stores import IUserStore, IRoleStore
from fastapi_identity.token_provider import (
    IUserTwoFactorTokenProvider,
    DefaultTokenProvider,
    EmailTokenProvider,
    PhoneNumberTokenProvider
)
from fastapi_identity.types import TUser, TRole, DependencyCallable
from fastapi_identity.user_claims_principal_factory import IUserClaimsPrincipalFactory
from fastapi_identity.user_validator import IUserValidator


class IdentityBuilder:
    def __init__(self, user: type[TUser], role: type[TRole], services: dict):
        self.user = user
        self.role = role
        self.services = services

    def add_user_validator(self, get_validators: DependencyCallable[Iterable[IUserValidator[TUser]]]):
        self.services[depends.IUserValidators] = get_validators
        return self

    def add_claims_principal_factory(self, get_factory: DependencyCallable[IUserClaimsPrincipalFactory[TUser]]):
        self.services[depends.IUserClaimsPrincipalFactory] = get_factory
        return self

    def add_error_describer(self, get_describer: DependencyCallable[IdentityErrorDescriber]):
        self.services[depends.IdentityErrorDescriber] = get_describer
        return self

    def add_password_validator(self, get_validators: DependencyCallable[Iterable[IPasswordValidator[TUser]]]):
        self.services[depends.IPasswordValidators] = get_validators
        return self

    def add_user_store(self, get_store: DependencyCallable[IUserStore[TUser]]):
        self.services[depends.IUserStore] = get_store
        return self

    def add_user_manager[TUserManager](self, get_manager: DependencyCallable[TUserManager]):
        self.services[depends.UserManager] = get_manager
        return self

    def add_role_validator(self, get_validators: DependencyCallable[Iterable[IRoleValidator[TRole]]]):
        self.services[depends.IRoleValidators] = get_validators
        return self

    def add_role_store(self, get_store: DependencyCallable[IRoleStore[TRole]]):
        self.services[depends.IRoleStore] = get_store
        return self

    def add_role_manager[TRoleManager](self, get_manager: DependencyCallable[TRoleManager]):
        self.services[depends.RoleManager] = get_manager
        return self

    def add_user_confirmation(self, get_confirmation: DependencyCallable[IUserConfirmation[TUser]]):
        self.services[depends.IUserConfirmation] = get_confirmation
        return self

    def add_token_provider(self, provider_name: str, provider: IUserTwoFactorTokenProvider[TUser]):
        self.services[depends.IdentityOptions]().Tokens.PROVIDER_MAP[provider_name] = provider
        return self

    def add_default_token_providers(self):
        self.add_token_provider(TokenOptions.DEFAULT_PROVIDER, DefaultTokenProvider())
        self.add_token_provider(TokenOptions.DEFAULT_EMAIL_PROVIDER, EmailTokenProvider())
        self.add_token_provider(TokenOptions.DEFAULT_PHONE_PROVIDER, PhoneNumberTokenProvider())
        return self

    def add_signin_manager(self, get_manager: DependencyCallable[SignInManager[TUser]]):
        self.services[depends.SignInManager] = get_manager
        return self
