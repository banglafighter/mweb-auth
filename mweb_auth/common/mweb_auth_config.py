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
    INVALID_OPERATOR_MSG = "Missing or invalid operator information"
    PASSWORD_MISMATCH_ERROR_MSG = "New password and confirm password do not match"
    DATA_VALIDATION_ERROR_MSG = "Data validation error!"
    USERNAME_MIN_LENGTH_ERROR_MSG = "Username must be at least {} characters long"
    USERNAME_MAX_LENGTH_ERROR_MSG = "Username must be at most {} characters long"
    USERNAME_INVALID_CHAR_ERROR_MSG = "Username can only contain lowercase letters (a–z), numbers (0–9), dots (.), and hyphens (-)"
    PASSWORD_MIN_LENGTH_ERROR_MSG = "Password must be at least {} characters long"

    # Configuration
    SKIP_EXACT_URLS_FROM_AUTH: list = []
    SKIP_PREFIXES_URL_FROM_AUTH: list = []
