from mweb_auth.data.mweb_auth_enum import OperatorStatus, OperatorAccessType
from mweb_crud.data_transfer import MWebBaseDTO, dto


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