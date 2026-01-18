from mw_common import HTTPStatusCode
from mweb_auth.common.mweb_auth_config import MWebAuthConfig
from mweb_auth.common.mweb_auth_hook import MWebAuthHook
from mweb_auth.common.mweb_auth_registry import MWebAuthRegistry
from mweb_auth.connect.mweb_auth_base_interceptor import MWebAuthBaseInterceptor
from mweb_auth.security.mweb_jwt import MWebJWT
from mweb_crud.crud import RequestContext, ResponseMaker
from mweb_crud.crud.mweb_request_context import MWebRequestURLInfo
from mweb_crud.randr import MWebRESTResponseCode


class MWebAuthInterceptor(MWebAuthBaseInterceptor):
    _request_context: RequestContext = None
    _response_maker: ResponseMaker = None
    _request_url_info: MWebRequestURLInfo = None
    _mweb_jwt: MWebJWT = MWebJWT()

    def __init__(self):
        self._request_context = RequestContext()
        self._response_maker = ResponseMaker()

    def get_relative_url(self):
        relative_url = self._request_url_info.relativeURL
        if not relative_url:
            relative_url = self._request_url_info.relativeURLWithParam
        return relative_url

    def check_skip_url_prefixes(self, request_url, url_list: list = None):
        for url in url_list:
            if request_url.startswith(url):
                return True
        return False

    async def is_url_skipped(self, tenant: str = "default") -> bool:
        relative_url = self.get_relative_url()
        skip_exact_urls = MWebAuthRegistry.get_skip_exact_urls(tenant=tenant)
        skip_url_prefixes = MWebAuthRegistry.get_skip_prefixes(tenant=tenant)
        checker = MWebAuthHook.auth_skip_url_checker()
        if checker is not None:
            return await checker.check(relative_url=relative_url, skip_exact_urls=skip_exact_urls, skip_prefixes=skip_url_prefixes)
        if relative_url in skip_exact_urls or self.check_skip_url_prefixes(relative_url, url_list=skip_url_prefixes):
            return True
        return False

    async def get_error_response(self, message: str | None = None):
        if not message:
            message = MWebAuthConfig.NOT_AUTHORIZED_MSG
        return await self._response_maker.error(message, code=MWebRESTResponseCode.unauthorized, http_code=HTTPStatusCode.UNAUTHORIZED)

    def is_rest_request(self) -> bool:
        relative_url = self.get_relative_url()
        if relative_url.startswith(MWebAuthConfig.REST_URL_START_WITH):
            return True
        return False

    def is_assets_request(self) -> bool:
        relative_url = self.get_relative_url()
        if relative_url.startswith(MWebAuthConfig.ASSET_URL_START_WITH):
            return True
        return False

    async def check_rest_auth(self, is_assets_request: bool = False):
        bearer_token = self._request_context.extract_bearer_token()
        if not bearer_token:
            bearer_token = self._request_context.get_query_param("auth-token")
            if not bearer_token:
                return await self.get_error_response()

        payload = self._mweb_jwt.validate_token(bearer_token)
        if not payload:
            return await self.get_error_response()

        if is_assets_request:
            return None

        acl_checker = MWebAuthHook.auth_rest_acl_interceptor()
        if acl_checker:
            return await acl_checker.intercept(request_url_info=self._request_url_info, payload=payload)
        return None

    async def check_auth(self):
        if self.is_rest_request():
            if not MWebAuthConfig.ENABLE_API_AUTH:
                return None
            return await self.check_rest_auth()
        elif self.is_assets_request():
            return await self.check_rest_auth(is_assets_request=True)
        else:
            if not MWebAuthConfig.ENABLE_NONE_API_AUTH:
                return None

        return await self.get_error_response(message=MWebAuthConfig.AUTHENTICATION_FAILED_MSG)

    async def intercept(self):
        self._request_url_info = self._request_context.extract_request_url_info()

        if self._request_url_info.method == 'OPTIONS':
            return await self._response_maker.success(content="Allowed")

        if not await self.is_url_skipped():
            return await self.check_auth()
        return None
