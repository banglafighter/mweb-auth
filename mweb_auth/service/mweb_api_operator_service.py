from mw_common import MwUtil, DataUtil
from mweb.saas.mweb_saas import MWebSaaS, MWebSaaSConst
from mweb_auth.common.mweb_auth_config import MWebAuthConfig
from mweb_auth.common.mweb_auth_hook import MWebAuthHook
from mweb_auth.default_dto import RefreshTokenDefaultDTO
from mweb_auth.default_dto.mweb_auth_dtos import MWebAuthDTOs
from mweb_auth.default_model import OperatorTokenDefault, MWebAuthModels
from mweb_auth.security.mweb_jwt import MWebJWT
from mweb_auth.service import MWebOperatorService
from mweb_crud.common import MWebCRUDException
from mweb_crud.crud import CRUDManager
from mweb_crud.randr import MWebRESTResponseCode


class MWebAPIOperatorService:
    OPERATOR = "operator"
    TOKEN = "token"
    mweb_jwt: MWebJWT = None
    crud_manager: CRUDManager = None
    operator_token: type[OperatorTokenDefault] = None
    mweb_operator_service: MWebOperatorService = None

    def __init__(self):
        self.mweb_jwt = MWebJWT()
        self.operator_token = MWebAuthModels.operator_token()
        self.crud_manager = CRUDManager(model=self.operator_token)
        self.mweb_operator_service = MWebOperatorService()

    async def get_operator_token_by_operator_id(self, operator_id, raise_error: bool = True) -> OperatorTokenDefault | None:
        query = self.operator_token.query.where(self.operator_token.tokenOwnerId == operator_id)
        return await self.crud_manager.get_first(query=query, raise_error=raise_error, message=MWebAuthConfig.OPERATOR_TOKEN_NOT_FOUND_MSG)

    async def get_operator_token_by_token(self, token, raise_error: bool = True):
        query = self.operator_token.query.where(self.operator_token.token == token)
        return await self.crud_manager.get_first(query=query, raise_error=raise_error, message=MWebAuthConfig.OPERATOR_TOKEN_NOT_FOUND_MSG)

    async def create_or_update_db_refresh_token(self, operator_id, uuid=None) -> OperatorTokenDefault | None:
        existing_token = await self.get_operator_token_by_operator_id(operator_id, raise_error=False)
        if uuid and (not existing_token or existing_token.token != uuid):
            return None

        if not existing_token:
            existing_token = self.operator_token( tokenOwnerId=operator_id)

        existing_token.token = MwUtil.uuid()
        await existing_token.save()
        return existing_token

    async def get_access_token(self, operator_id, payload: dict = None):
        operator = await self.mweb_operator_service.get_operator_by_id(operator_id)
        if not operator:
            return None

        if not payload:
            payload = {}
        payload[self.OPERATOR] = operator.id
        tkey = MWebSaaS.get_tenant_key()
        if tkey:
            payload[MWebSaaSConst.TENANT_KEY] = tkey
        return self.mweb_jwt.get_access_token(payload, iss=operator.uuid)

    async def get_refresh_token(self, operator_id, payload: dict = None):
        operator = await self.mweb_operator_service.get_operator_by_id(operator_id)
        if not operator:
            return None

        if not payload:
            payload = {}
        payload[self.OPERATOR] = operator.id

        db_token = await self.create_or_update_db_refresh_token(operator_id)
        if not db_token:
            return None
        payload[self.TOKEN] = db_token.token
        tkey = MWebSaaS.get_tenant_key()
        if tkey:
            payload[MWebSaaSConst.TENANT_KEY] = tkey
        return self.mweb_jwt.get_refresh_token(payload, iss=operator.uuid)

    async def process_login_data(self, operator, response_dto=None):
        token = {
            "accessToken": await self.get_access_token(operator_id=operator.id),
            "refreshToken": await self.get_refresh_token(operator_id=operator.id)
        }
        response = {
            "operator": operator,
            "token": token
        }
        if response_dto:
            response_dict = response_dto.dump(response)
        else:
            response_dict = MWebAuthDTOs.login_response_dto(model=response)

        on_token_generation = MWebAuthHook.token_generation_interceptor()
        if on_token_generation:
            response = await on_token_generation.intercept(response=response_dict, operator=operator)
            if response:
                return response
        return response_dict

    async def refresh_token(self):
        data = await self.crud_manager.request.get_data(validator=RefreshTokenDefaultDTO())
        refresh_token = DataUtil.dict_value(data=data, key="refreshToken")
        return await self.access_token_by_refresh_token(refresh_token=refresh_token)


    async def access_token_by_refresh_token(self, refresh_token):
        jwt_payload = self.mweb_jwt.validate_token(token=refresh_token)
        operator_id = DataUtil.dict_value(jwt_payload, self.OPERATOR)
        token = DataUtil.dict_value(jwt_payload, self.TOKEN)
        if not jwt_payload or not operator_id or not token:
            raise MWebCRUDException(message=MWebAuthConfig.INVALID_TOKEN_MSG, error_code=MWebRESTResponseCode.invalid_token_code)

        operator_token = await self.get_operator_token_by_token(token=token, raise_error=False)
        if not operator_token:
            raise MWebCRUDException(message=MWebAuthConfig.TOKEN_EXPIRED_MSG, error_code=MWebRESTResponseCode.token_expired_code)

        access_token = await self.get_access_token(operator_id=operator_id)
        refresh_token = await self.get_refresh_token(operator_id=operator_id)
        if not access_token or not refresh_token:
            raise MWebCRUDException(message=MWebAuthConfig.TOKEN_GENERATION_ERROR_MSG, error_code=MWebRESTResponseCode.token_error_code)

        token = {
            "accessToken": access_token,
            "refreshToken": refresh_token
        }

        on_renew_token = MWebAuthHook.token_renewal_interceptor()
        if on_renew_token is not None:
            response = await on_renew_token.intercept(token=token, jwt_payload=jwt_payload)
            if response:
                return response

        return await self.crud_manager.response.success(content=token)
