from abc import ABC, abstractmethod
from mweb_auth.default_model import OperatorDefault
from mweb_crud.crud.mweb_request_context import MWebRequestURLInfo


class MWebAuthSkipURLChecker(ABC):
    @abstractmethod
    async def check(self, relative_url: str, skip_exact_urls: list, skip_prefixes: list) -> bool: ...


class MWebAuthRestAclInterceptor(ABC):
    @abstractmethod
    async def intercept(self, request_url_info: MWebRequestURLInfo, payload: dict): ...


class MWebLoginInterceptor(ABC):
    @abstractmethod
    async def intercept(self, operator: OperatorDefault, login_data: dict): ...


class MWebCustomLoginHandler(ABC):
    @abstractmethod
    async def login(self, login_data: dict) -> OperatorDefault: ...


class MWebTokenGenerationInterceptor(ABC):
    @abstractmethod
    async def intercept(self, response: dict, operator: OperatorDefault): ...


class MWebTokenRenewalInterceptor(ABC):

    @abstractmethod
    async def perform(self, token: dict, jwt_payload: dict) -> dict: ...


class MWebForgotPasswordRequestNotifier(ABC):
    @abstractmethod
    async def notify(self, operator: OperatorDefault, reset_token: str) -> bool: ...


class MWebResetPasswordFailureNotifier(ABC):
    @abstractmethod
    async def notify(self, reset_token: str): ...


class MWebResetPasswordSuccessNotifier(ABC):
    @abstractmethod
    async def notify(self, operator: OperatorDefault): ...


class MWebLoginFailureNotifier(ABC):
    @abstractmethod
    async def notify(self, operator: OperatorDefault, login_data: dict): ...


class MWebLoginSuccessNotifier(ABC):
    @abstractmethod
    async def notify(self, operator: OperatorDefault, login_data: dict): ...


class MWebOperatorCreationNotifier(ABC):
    @abstractmethod
    async def notify(self, operator: OperatorDefault): ...
