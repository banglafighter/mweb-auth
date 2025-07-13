class MWebAuthConfig:
    # JWT
    JWT_SECRET: str = "PleaseChangeTheToken"
    JWT_REFRESH_TOKEN_VALIDITY_MIN: int = 45
    JWT_ACCESS_TOKEN_VALIDITY_MIN: int = 30
    RESET_PASSWORD_TOKEN_VALID_MIN: int = 150
