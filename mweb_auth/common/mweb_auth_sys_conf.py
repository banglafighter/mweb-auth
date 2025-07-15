from mweb import MWebSystemConfig
from mweb_auth.default_model import OperatorDefaultBase, OperatorTokenDefault
from mweb_crud.data_transfer import MWebBaseDTO


class MWebAuthSysConf(MWebSystemConfig):
    OPERATOR_MODEL: type[OperatorDefaultBase] = None
    OPERATOR_TOKEN_MODEL: type[OperatorTokenDefault] = None

    LOGIN_DTO: type[MWebBaseDTO] = None
    LOGIN_RESPONSE_DTO: type[MWebBaseDTO] = None
    FORGOT_PASSWORD_DTO: type[MWebBaseDTO] = None
    OPERATOR_CREATE_DTO: type[MWebBaseDTO] = None
    OPERATOR_UPDATE_DTO: type[MWebBaseDTO] = None
    OPERATOR_READ_DTO: type[MWebBaseDTO] = None
    REGISTRATION_DTO: type[MWebBaseDTO] = None
