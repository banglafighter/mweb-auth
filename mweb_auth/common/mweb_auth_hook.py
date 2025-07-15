from typing import Type, TypeVar, cast
from mweb_auth.connect import MWebAuthSkipURLChecker, MWebAuthRestAclInterceptor, MWebLoginInterceptor, \
    MWebCustomLoginHandler, MWebTokenGenerationInterceptor, MWebTokenRenewalInterceptor, \
    MWebForgotPasswordRequestNotifier, MWebResetPasswordFailureNotifier, MWebResetPasswordSuccessNotifier, \
    MWebLoginFailureNotifier, MWebLoginSuccessNotifier, MWebOperatorCreationNotifier
from mweb_auth.connect.mweb_auth_base_interceptor import MWebAuthBaseInterceptor

T = TypeVar('T')


class MWebAuthHook:
    AUTH_SKIP_URL_CHECKER: MWebAuthSkipURLChecker = None
    AUTH_REST_ACL_INTERCEPTOR: MWebAuthRestAclInterceptor = None
    AUTH_INTERCEPTOR: MWebAuthBaseInterceptor = None

    # Interceptors
    LOGIN_INTERCEPTOR: MWebLoginInterceptor = None
    CUSTOM_LOGIN_HANDLER: MWebCustomLoginHandler = None
    TOKEN_GENERATION_INTERCEPTOR: MWebTokenGenerationInterceptor = None
    TOKEN_RENEWAL_INTERCEPTOR: MWebTokenRenewalInterceptor = None

    # Auth Notifications
    FORGOT_PASSWORD_REQUEST_NOTIFIER: MWebForgotPasswordRequestNotifier = None
    RESET_PASSWORD_FAILURE_NOTIFIER: MWebResetPasswordFailureNotifier = None
    RESET_PASSWORD_SUCCESS_NOTIFIER: MWebResetPasswordSuccessNotifier = None
    LOGIN_FAILURE_NOTIFIER: MWebLoginFailureNotifier = None
    LOGIN_SUCCESS_NOTIFIER: MWebLoginSuccessNotifier = None
    OPERATOR_CREATION_NOTIFIER: MWebOperatorCreationNotifier = None

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

    @classmethod
    def auth_interceptor(cls) -> MWebAuthBaseInterceptor | None:
        return cls.get_hook('AUTH_INTERCEPTOR', MWebAuthBaseInterceptor)

    @classmethod
    def login_interceptor(cls) -> MWebLoginInterceptor | None:
        return cls.get_hook('LOGIN_INTERCEPTOR', MWebLoginInterceptor)

    @classmethod
    def custom_login_handler(cls) -> MWebCustomLoginHandler | None:
        return cls.get_hook('CUSTOM_LOGIN_HANDLER', MWebCustomLoginHandler)

    @classmethod
    def token_generation_interceptor(cls) -> MWebTokenGenerationInterceptor | None:
        return cls.get_hook('TOKEN_GENERATION_INTERCEPTOR', MWebTokenGenerationInterceptor)

    @classmethod
    def token_renewal_interceptor(cls) -> MWebTokenRenewalInterceptor | None:
        return cls.get_hook('TOKEN_RENEWAL_INTERCEPTOR', MWebTokenRenewalInterceptor)

    @classmethod
    def forgot_password_request_notifier(cls) -> MWebForgotPasswordRequestNotifier | None:
        return cls.get_hook('FORGOT_PASSWORD_REQUEST_NOTIFIER', MWebForgotPasswordRequestNotifier)

    @classmethod
    def reset_password_failure_notifier(cls) -> MWebResetPasswordFailureNotifier | None:
        return cls.get_hook('RESET_PASSWORD_FAILURE_NOTIFIER', MWebResetPasswordFailureNotifier)

    @classmethod
    def reset_password_success_notifier(cls) -> MWebResetPasswordSuccessNotifier | None:
        return cls.get_hook('RESET_PASSWORD_SUCCESS_NOTIFIER', MWebResetPasswordSuccessNotifier)

    @classmethod
    def login_failure_notifier(cls) -> MWebLoginFailureNotifier | None:
        return cls.get_hook('LOGIN_FAILURE_NOTIFIER', MWebLoginFailureNotifier)

    @classmethod
    def login_success_notifier(cls) -> MWebLoginSuccessNotifier | None:
        return cls.get_hook('LOGIN_SUCCESS_NOTIFIER', MWebLoginSuccessNotifier)

    @classmethod
    def operator_creation_notifier(cls) -> MWebOperatorCreationNotifier | None:
        return cls.get_hook('OPERATOR_CREATION_NOTIFIER', MWebOperatorCreationNotifier)
