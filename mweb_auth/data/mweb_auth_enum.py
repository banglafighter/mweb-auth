from mweb_crud.data_transfer import BaseEnum


class OperatorStatus(BaseEnum):
    Active = "Active"
    Inactive = "Inactive"


class OperatorAccessType(BaseEnum):
    Operator = "Operator"
    Admin = "Admin"


class AuthBase(BaseEnum):
    EMAIL = "EMAIL"
    USERNAME = "USERNAME"
