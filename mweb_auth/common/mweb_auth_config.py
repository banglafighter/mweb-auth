class MWebAuthConfig:
    # JWT
    JWT_SECRET: str = "PleaseChangeTheToken"
    JWT_REFRESH_TOKEN_VALIDITY_MIN: int = 45
    JWT_ACCESS_TOKEN_VALIDITY_MIN: int = 30
    RESET_PASSWORD_TOKEN_VALID_MIN: int = 150

    # Authentication
    ENABLE_AUTH: bool = True

    # URL Specification
    REST_URL_START_WITH = "/api"
    ASSET_URL_START_WITH = "/assets"

    # Messages
    NOT_AUTHORIZED_MSG = "You are not authorized to access this resource"
    AUTHENTICATION_FAILED_MSG = "Authentication Failed"

    # Configuration
    SKIP_EXACT_URLS_FROM_AUTH: list = []
    SKIP_PREFIXES_URL_FROM_AUTH: list = []
