from mweb import MWebBase, MWebConfig, MWebSystemConfig, MWebHook, MWebUtil
from .common.mweb_auth_registry import MWebAuthRegistry
from .default_dto.mweb_auth_dtos import MWebAuthDTOs
from .default_model import MWebAuthModels
from .security.mweb_auth_interceptor import MWebAuthInterceptor


class MWebAuthModule:

    def merge_system_config(self, system_config: MWebSystemConfig):
        from mweb_auth.common.mweb_auth_sys_conf import MWebAuthSysConf
        MWebUtil.copy_config_property(source=system_config, destination=MWebAuthSysConf)

    def merge_hook(self, hook: MWebHook):
        from mweb_auth.common.mweb_auth_hook import MWebAuthHook
        MWebUtil.copy_config_property(source=hook, destination=MWebAuthHook)

    def merge_config(self, config: MWebConfig):
        from mweb_auth.common.mweb_auth_config import MWebAuthConfig
        MWebUtil.copy_config_property(source=config, destination=MWebAuthConfig)

    def register(self, mweb_app: MWebBase, config: MWebConfig, hook: MWebHook, system_config: MWebSystemConfig):
        self.merge_system_config(system_config=system_config)
        self.merge_config(config=config)
        self.merge_hook(hook=hook)

        # Initialize Model
        MWebAuthModels.init_models()
        MWebAuthDTOs.init_dtos()

        self.register_auth_interceptor(mweb_app=mweb_app)

    def register_auth_interceptor(self, mweb_app: MWebBase):
        from mweb_auth.common.mweb_auth_config import MWebAuthConfig
        from mweb_auth.common.mweb_auth_hook import MWebAuthHook

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
