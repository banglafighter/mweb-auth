from mweb_auth.data.mweb_auth_enum import OperatorStatus, OperatorAccessType
from mweb_auth.util import MWebSecurityUtil
from mweb_crud.data_transfer import MWebBaseDTO, dto, validates_schema


class LoginTokenDefaultDTO(MWebBaseDTO):
    accessToken = dto.String(dump_only=True)
    refreshToken = dto.String(dump_only=True)


class OperatorReadDefaultDTO(MWebBaseDTO):
    name = dto.String(required=True, error_messages={"required": "Please enter name"})
    email = dto.Email(required=True, error_messages={"required": "Please enter email."})
    username = dto.String(required=True, error_messages={"required": "Please enter username."})
    status = dto.Enum(OperatorStatus, required=True, error_messages={"required": "Please select status"})
    accessType = dto.Enum(OperatorAccessType, required=True, error_messages={"required": "Please select access"})
    profilePhoto = dto.String(allow_none=True)
    coverPhoto = dto.String(allow_none=True)


class ResetPasswordDefaultDTO(MWebBaseDTO):
    newPassword = dto.String(required=True, error_messages={"required": "Please enter new password."})
    confirmPassword = dto.String(required=True, error_messages={"required": "Please enter confirm password."})
    token = dto.String(required=True, error_messages={"required": "Please enter token."})

    @validates_schema
    def validate_schema(self, data, **kwargs):
        MWebSecurityUtil.validate_password_match(data=data)


class RefreshTokenDefaultDTO(MWebBaseDTO):
    refreshToken = dto.String(required=True, error_messages={"required": "Please enter refresh token."})


class ForgotPasswordBaseDefaultDTO(MWebBaseDTO):
    username = dto.Email(required=True, error_messages={"required": "Please enter username."})


class LoginResponseDefaultDTO(MWebBaseDTO):
    token = dto.Nested(LoginTokenDefaultDTO())
    operator = dto.Nested(OperatorReadDefaultDTO())
