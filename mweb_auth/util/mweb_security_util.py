import re
import bcrypt
from mw_common import DataUtil
from mweb_crud.common import MWebCRUDException


class MWebSecurityUtil:

    @staticmethod
    def hash_password(password, salt=None):
        if not salt:
            salt = bcrypt.gensalt()
        if password:
            password = password.encode('utf8')
        hashed = bcrypt.hashpw(password, salt)
        if hashed:
            hashed = hashed.decode()
        return hashed

    @staticmethod
    def verify_password_hash(password, hashed):
        if password:
            password = password.encode('utf8')
        if hashed and isinstance(hashed, str):
            hashed = hashed.encode('utf8')
        if bcrypt.checkpw(password, hashed):
            return True
        return False

    @staticmethod
    def validate_password_match(data: dict, new_pass_key="newPassword", confirm_pass_key="confirmPassword", raise_error=True, error_message: str | None = None):
        from mweb_auth.common.mweb_auth_config import MWebAuthConfig

        if not error_message:
            error_message = MWebAuthConfig.PASSWORD_MISMATCH_ERROR_MSG

        new_password = DataUtil.dict_value(data=data, key=new_pass_key)
        confirm_password = DataUtil.dict_value(data=data, key=confirm_pass_key)
        if new_password and confirm_password and new_password == confirm_password:
            return True
        if not raise_error:
            return False
        raise MWebCRUDException(message=MWebAuthConfig.DATA_VALIDATION_ERROR_MSG, details={confirm_pass_key: error_message})

    @staticmethod
    def validate_username(data: dict, min_length: int | None = None, max_length: int | None = None, raise_error=True) -> bool | str:
        from mweb_auth.common.mweb_auth_config import MWebAuthConfig

        username = DataUtil.dict_value(data=data, key="username")
        if not username:
            return False

        if not min_length:
            min_length = 6

        if not max_length:
            max_length = 20

        message: str | None = None
        username_length = len(username)

        if username_length < min_length:
            message = MWebAuthConfig.USERNAME_MIN_LENGTH_ERROR_MSG.format(min_length)
        elif username_length > max_length:
            message = MWebAuthConfig.USERNAME_MAX_LENGTH_ERROR_MSG.format(max_length)
        elif not re.match("[a-zA-Z0-9.-]+$", username):
            message = MWebAuthConfig.USERNAME_INVALID_CHAR_ERROR_MSG

        if message and raise_error:
            raise MWebCRUDException(message=MWebAuthConfig.DATA_VALIDATION_ERROR_MSG, details={"username": message})

        if not message:
            return True
        return message

    @staticmethod
    def validate_password(data: dict, min_length: int | None = None, raise_error=True, dict_key: str | None = None) -> bool | str:
        from mweb_auth.common.mweb_auth_config import MWebAuthConfig

        if not dict_key:
            dict_key = "password"

        password = DataUtil.dict_value(data=data, key=dict_key)
        if not password:
            return False

        if not min_length:
            min_length = 6

        message: str | None = None
        password_length = len(password)

        if password_length < min_length:
            message = MWebAuthConfig.PASSWORD_MIN_LENGTH_ERROR_MSG.format(min_length)

        if message and raise_error:
            raise MWebCRUDException(message=MWebAuthConfig.DATA_VALIDATION_ERROR_MSG, details={"password": message})

        if not message:
            return True
        return message

    @classmethod
    def is_valid_local_bd_mobile(cls, data: dict, field_name="mobile", error_message=None) -> bool:
        if not error_message:
            error_message = "Invalid mobile number"

        mobile = DataUtil.dict_value(data=data, key=field_name)
        bd_local_mobile_regex = re.compile(r"^01[3-9]\d{8}$")
        is_valid_mobile = bool(bd_local_mobile_regex.match(mobile.strip()))
        if is_valid_mobile:
            return True
        raise MWebCRUDException(message=error_message, details={field_name: error_message})
