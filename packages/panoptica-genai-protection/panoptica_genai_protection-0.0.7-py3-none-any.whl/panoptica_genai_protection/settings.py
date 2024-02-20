
# auth settings
ESCHER_TOKEN_URL = '/apisec/escher/token_management/serviceapi/apisec_token_management/token'
SCOPE = 'global/services/portshift_request'
SIGN_URL = '/api/serviceMe'  # we sign a fixed endpoint serviceME rather than the explicit request
JWT_TIMEOUT_MS = 1800000  # 30 minutes