from mweb_auth.default_model import OperatorDefaultBase, OperatorTokenDefault


class MWebAuthModels:
    _operator: type[OperatorDefaultBase] = None
    _operator_token: type[OperatorTokenDefault] = None

    @classmethod
    def operator(cls) -> type[OperatorDefaultBase]:
        return cls._operator

    @classmethod
    def operator_token(cls) -> type[OperatorTokenDefault]:
        return cls._operator_token

    @classmethod
    def init_models(cls):
        from mweb_auth.common.mweb_auth_sys_conf import MWebAuthSysConf

        # Init Operator Model
        if MWebAuthSysConf.OPERATOR_MODEL:
            cls._operator = MWebAuthSysConf.OPERATOR_MODEL
        else:
            class Operator(OperatorDefaultBase):
                pass

            cls._operator = Operator

        # Init Operator Token Model
        if MWebAuthSysConf.OPERATOR_TOKEN_MODEL:
            cls._operator_token = MWebAuthSysConf.OPERATOR_TOKEN_MODEL
        else:
            class OperatorToken(OperatorTokenDefault):
                pass

            cls._operator_token = OperatorToken
