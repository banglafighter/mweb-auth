from abc import ABC, abstractmethod
from mweb_crud.crud.mweb_request_context import MWebRequestURLInfo


class MWebAuthSkipURLChecker(ABC):

    @abstractmethod
    def check(self, relative_url: str, skip_exact_urls: list, skip_prefixes: list) -> bool: ...


class MWebAuthRestAclInterceptor(ABC):

    @abstractmethod
    async def intercept(self, request_url_info: MWebRequestURLInfo, payload: dict): ...
