from mw_common import DataUtil
from mweb_auth.common.mweb_auth_config import MWebAuthConfig
from mweb_auth.security.mweb_jwt import MWebJWT
from mweb_crud.common import MWebCRUDException
from mweb_crud.crud import RequestContext


class MWebRESTUtil:
    _request_context: RequestContext = None
    _mweb_jwt: MWebJWT = None

    def __init__(self):
        self._request_context = RequestContext()
        self._mweb_jwt = MWebJWT()

    @classmethod
    def extract_auth_payload(cls):
        bearer_token = cls._request_context.extract_bearer_token()
        return cls._mweb_jwt.validate_token(token=bearer_token)

    @classmethod
    def operator_id_from_payload(cls, error_message: str | None = None, payload: dict | None = None):
        if not payload:
            payload = cls.extract_auth_payload()

        if not error_message:
            error_message = MWebAuthConfig.INVALID_OPERATOR_MSG

        operator_id = DataUtil.dict_value(payload, "operator")
        if operator_id is None:
            raise MWebCRUDException(message=error_message)
        return operator_id
