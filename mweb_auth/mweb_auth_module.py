from mweb import MWebBase, MWebConfig
from mweb.engine.mweb_hook import MWebHook
from mweb.engine.mweb_util import MWebUtil
from mweb_auth.common.mweb_auth_config import MWebAuthConfig
from mweb_auth.common.mweb_auth_hook import MWebAuthHook
from mweb_auth.common.mweb_auth_registry import MWebAuthRegistry
from mweb_auth.security.mweb_auth_interceptor import MWebAuthInterceptor


class MWebAuthModule:

    def register(self, mweb_app: MWebBase, config: MWebConfig, hook: MWebHook):
        MWebUtil.copy_config_property(source=config, destination=MWebAuthConfig)
        MWebUtil.copy_config_property(source=hook, destination=MWebAuthHook)

        self.register_auth_interceptor(mweb_app=mweb_app)

    def register_auth_interceptor(self, mweb_app: MWebBase):
        if not MWebAuthConfig.ENABLE_AUTH or not mweb_app:
            return

        interceptor = MWebAuthHook.auth_interceptor()
        if not interceptor:
            MWebAuthHook.AUTH_INTERCEPTOR = MWebAuthInterceptor()

        if MWebAuthConfig.SKIP_EXACT_URLS_FROM_AUTH and isinstance(MWebAuthConfig.SKIP_EXACT_URLS_FROM_AUTH, list):
            MWebAuthRegistry.add_exact_url_list_in_skip(urls=MWebAuthConfig.SKIP_EXACT_URLS_FROM_AUTH)

        if MWebAuthConfig.SKIP_PREFIXES_URL_FROM_AUTH and isinstance(MWebAuthConfig.SKIP_PREFIXES_URL_FROM_AUTH, list):
            MWebAuthRegistry.add_prefix_url_list_in_skip(urls=MWebAuthConfig.SKIP_PREFIXES_URL_FROM_AUTH)

        mweb_app.before_request_funcs.setdefault(None, []).append(MWebAuthHook.AUTH_INTERCEPTOR.intercept)
