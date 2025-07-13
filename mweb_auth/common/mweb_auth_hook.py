from typing import Type, TypeVar, cast
from mweb_auth.connect.mweb_auth_connector import MWebAuthSkipURLChecker, MWebAuthRestAclInterceptor

T = TypeVar('T')


class MWebAuthHook:
    AUTH_SKIP_URL_CHECKER: MWebAuthSkipURLChecker = None
    AUTH_REST_ACL_INTERCEPTOR: MWebAuthRestAclInterceptor = None

    @classmethod
    def get_hook(cls, hook_name: str, hook_type: Type[T], default=None) -> T | None:
        if hasattr(cls, hook_name):
            hook = getattr(cls, hook_name)
            if hook is None and isinstance(default, hook_type):
                return cast(T, getattr(cls, hook_name))
        return default

    @classmethod
    def auth_skip_url_checker(cls) -> MWebAuthSkipURLChecker | None:
        return cls.get_hook('AUTH_SKIP_URL_CHECKER', MWebAuthSkipURLChecker)

    @classmethod
    def auth_rest_acl_interceptor(cls) -> MWebAuthRestAclInterceptor | None:
        return cls.get_hook('AUTH_REST_ACL_INTERCEPTOR', MWebAuthRestAclInterceptor)
