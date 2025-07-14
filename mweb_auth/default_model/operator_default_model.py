from mweb_auth.util import MWebSecurityUtil
from mweb_orm import MWebModel
from mweb_orm.orm import mweb_orm


class OperatorDefaultBase(MWebModel):
    __abstract__ = True
    email = mweb_orm.Column("email", mweb_orm.String(100), unique=True, index=True)
    username = mweb_orm.Column("username", mweb_orm.String(100), unique=True, index=True)
    password_hash = mweb_orm.Column("password_hash", mweb_orm.String(400), nullable=False, index=True)
    token = mweb_orm.Column("token", mweb_orm.String(200))
    isVerified = mweb_orm.Column("is_verified", mweb_orm.Boolean, default=True)

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, password):
        self.password_hash = MWebSecurityUtil.hash_password(password)

    def verify_password(self, password) -> bool:
        return MWebSecurityUtil.validate_password(password, self.password_hash)


class OperatorDefault(OperatorDefaultBase):
    __abstract__ = True
    firstName = mweb_orm.Column("first_name", mweb_orm.String(100))
    lastName = mweb_orm.Column("last_name", mweb_orm.String(100))
    name = mweb_orm.Column("name", mweb_orm.String(100))
    status = mweb_orm.Column("status", mweb_orm.String(25), default="Active")
    accessType = mweb_orm.Column("access_type", mweb_orm.String(25), default="Operator")
    profilePhoto = mweb_orm.Column("profile_photo", mweb_orm.String(200))
    coverPhoto = mweb_orm.Column("cover_photo", mweb_orm.String(200))
