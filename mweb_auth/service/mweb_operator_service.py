from mw_common import DataUtil
from mweb_auth.common.mweb_auth_config import MWebAuthConfig
from mweb_auth.common.mweb_auth_hook import MWebAuthHook
from mweb_auth.data.mweb_auth_enum import AuthBase
from mweb_auth.default_model import OperatorTokenDefault, OperatorDefaultBase, MWebAuthModels, OperatorDefault
from mweb_crud.common import MWebCRUDException
from mweb_crud.crud import CRUDManager


class MWebOperatorService:
    operator_crud_manager: CRUDManager = None
    operator: type[OperatorDefaultBase] = None
    operator_token: type[OperatorTokenDefault] = None

    def __init__(self):
        self.operator = MWebAuthModels.operator()
        self.operator_token = MWebAuthModels.operator_token()
        self.operator_crud_manager = CRUDManager(model=self.operator)

    async def get_operator_by_email(self, email: str, raise_error: bool = True) -> OperatorDefaultBase | None:
        query = self.operator.query.where(self.operator.email == email)
        return await self.operator_crud_manager.get_first(query=query, raise_error=raise_error, message=MWebAuthConfig.OPERATOR_NOT_FOUND_MSG)

    async def get_operator_by_username(self, username: str, raise_error: bool = True) -> OperatorDefaultBase | None:
        query = self.operator.query.where(self.operator.username == username)
        return await self.operator_crud_manager.get_first(query=query, raise_error=raise_error, message=MWebAuthConfig.OPERATOR_NOT_FOUND_MSG)

    async def get_operator_by_id(self, record_id: int, raise_error: bool = True) -> OperatorDefaultBase | None:
        return await self.operator_crud_manager.get_by_id(record_id=record_id, raise_error=raise_error, message=MWebAuthConfig.OPERATOR_NOT_FOUND_MSG)

    async def get_operator_by_uuid(self, uuid: str, raise_error: bool = True) -> OperatorDefaultBase | None:
        query = self.operator.query.where(self.operator.uuid == uuid)
        return await self.operator_crud_manager.get_first(query=query, raise_error=raise_error, message=MWebAuthConfig.OPERATOR_NOT_FOUND_MSG)

    async def get_operator_by_token(self, token: str, raise_error: bool = True) -> OperatorDefaultBase | None:
        query = self.operator.query.where(self.operator.token == token)
        return await self.operator_crud_manager.get_first(query=query, raise_error=raise_error, message=MWebAuthConfig.OPERATOR_NOT_FOUND_MSG)

    async def get_operator_from_data(self, dict_data: dict) -> OperatorDefaultBase | None:
        auth_base = MWebAuthConfig.SYSTEM_AUTH_BASE
        if auth_base == AuthBase.EMAIL:
            email = DataUtil.dict_value(dict_data, "email")
            return await self.get_operator_by_email(email, raise_error=False)
        elif auth_base == AuthBase.USERNAME:
            username = DataUtil.dict_value(dict_data, "username")
            return await self.get_operator_by_username(username, raise_error=False)
        return None

    async def authenticate_operator(self, login_data: dict):
        password = DataUtil.dict_value(login_data, "password")
        if not password:
            return None
        operator = await self.get_operator_from_data(dict_data=login_data)
        if operator and operator.verify_password(password):
            return operator
        return None

    async def login(self, login_data: dict):
        custom_login = MWebAuthHook.custom_login_handler()
        if custom_login:
            operator = await custom_login.login(login_data=login_data)
        else:
            operator = await self.authenticate_operator(login_data=login_data)
        return await self.fire_hooks(operator=operator, login_data=login_data)

    async def fire_hooks(self, operator: OperatorDefault, login_data: dict):
        on_login = MWebAuthHook.login_interceptor()
        if not operator:
            notify_on_login_failed = MWebAuthHook.login_failure_notifier()
            if notify_on_login_failed:
                await notify_on_login_failed.notify(operator=operator, login_data=login_data)
            raise MWebCRUDException(message=MWebAuthConfig.INVALID_CREDENTIALS_MSG)
        elif not operator.isVerified:
            raise MWebCRUDException(message=MWebAuthConfig.ACCOUNT_NOT_VERIFIED_MSG)

        if on_login:
            response = on_login.intercept(operator=operator, login_data=login_data)
            if response:
                return response

        notify_on_login_success = MWebAuthHook.login_success_notifier()
        if notify_on_login_success:
            await notify_on_login_success.notify(operator=operator, login_data=login_data)
        return operator
