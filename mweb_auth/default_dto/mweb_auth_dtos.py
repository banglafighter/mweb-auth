from mweb_auth.common.mweb_auth_sys_conf import MWebAuthSysConf
from mweb_auth.default_dto.mweb_auth_default_dto import LoginResponseDefaultDTO
from mweb_crud.data_transfer import MWebBaseDTO


class MWebAuthDTOs:
    _login_response_dto: type[MWebBaseDTO] = None

    @classmethod
    def login_response_dto(cls, model):
        return cls._login_response_dto().to_dict(model=model)

    @classmethod
    def init_dtos(cls):
        cls._set_dto(config_dto=MWebAuthSysConf.LOGIN_RESPONSE_DTO, default_dto=LoginResponseDefaultDTO, property_name="_login_response_dto")

    @classmethod
    def _set_dto(cls, config_dto: type[MWebBaseDTO], default_dto: type[MWebBaseDTO], property_name: str):
        set_dto = default_dto
        if config_dto is not None:
            set_dto = config_dto

        if hasattr(cls, property_name):
            setattr(cls, property_name, set_dto)
