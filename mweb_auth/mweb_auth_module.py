from mweb import MWebBase, MWebConfig
from mweb.engine.mweb_hook import MWebHook
from mweb.engine.mweb_util import MWebUtil
from mweb_auth.common.mweb_auth_config import MWebAuthConfig
from mweb_auth.common.mweb_auth_hook import MWebAuthHook


class MWebAuthModule:

    def register(self, mweb_app: MWebBase, config: MWebConfig, hook: MWebHook):
        MWebUtil.copy_config_property(source=config, destination=MWebAuthConfig)
        MWebUtil.copy_config_property(source=hook, destination=MWebAuthHook)
