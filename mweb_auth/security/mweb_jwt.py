import datetime
import jwt
from mweb.saas.mweb_saas_registry import MWebSaaSRegistry
from mweb_auth.common.mweb_auth_config import MWebAuthConfig


class MWebJWT:
    ALGORITHMS: str = "HS256"

    def get_token(self, exp: datetime, payload: dict = None, iss=None, secret=None):
        if not payload:
            payload = {}
        payload["exp"] = exp
        if iss:
            payload["iss"] = iss
        if not secret:
            secret = MWebSaaSRegistry.get_config(config_key="JWT_SECRET", default=MWebAuthConfig.JWT_SECRET)
        return jwt.encode(payload, secret, algorithm=self.ALGORITHMS)

    def get_access_token(self, payload: dict = None, iss=None):
        validity = self.get_access_token_validity()
        return self.get_token(validity, payload=payload, iss=iss)

    def get_refresh_token(self, payload: dict = None, iss=None):
        validity = self.get_refresh_token_validity()
        return self.get_token(validity, payload=payload, iss=iss)

    def validate_token(self, token: str, secret=None):
        try:
            if not token:
                return None
            if not secret:
                secret = MWebSaaSRegistry.get_config(config_key="JWT_SECRET", default=MWebAuthConfig.JWT_SECRET)
            return jwt.decode(token, secret, algorithms=[self.ALGORITHMS])
        except:
            return None

    def decode_token(self, token: str, check_signature: bool = True):
        try:
            if not token:
                return None
            options = {"verify_signature": check_signature}
            return jwt.decode(token, MWebSaaSRegistry.get_config(config_key="JWT_SECRET", default=MWebAuthConfig.JWT_SECRET), algorithms=[self.ALGORITHMS], options=options)
        except:
            return None

    def get_access_token_validity(self, minutes=None):
        if not minutes:
            minutes = MWebSaaSRegistry.get_config(config_key="JWT_ACCESS_TOKEN_VALIDITY_MIN", default=MWebAuthConfig.JWT_ACCESS_TOKEN_VALIDITY_MIN)
        return self.get_token_validity(minutes)

    def get_refresh_token_validity(self, minutes=None):
        if not minutes:
            minutes = MWebSaaSRegistry.get_config(config_key="JWT_REFRESH_TOKEN_VALIDITY_MIN", default=MWebAuthConfig.JWT_REFRESH_TOKEN_VALIDITY_MIN)
        return self.get_token_validity(minutes)

    def get_token_validity(self, minutes):
        return datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=minutes)
