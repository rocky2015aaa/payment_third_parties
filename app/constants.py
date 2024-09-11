ROUTE_GROUP = 'payment-gateway'

# exporter variables
AUTHORIZE_NET_API_LOGIN_ID = 'API_LOGIN_ID'
AUTHORIZE_NET_TRANSACTION_KEY = 'TRANSACTION_KEY'
HEARTLAND_BOLLETTA_API_USERNAME = 'bolletta_api_username'
HEARTLAND_BOLLETTA_API_PASSWORD = 'bolletta_api_password'
HEARTLAND_BDMS_MERCHANT_NAME = 'bdms_merchant_name'

# routes
ROUTE_AUTHORIZATION_TRANSACTION = '/%s/authorization/transaction' % ROUTE_GROUP
ROUTE_PAYMENT = '/%s/payment' % ROUTE_GROUP
ROUTE_REPORT = '/%s/report/{gateway_name}' % ROUTE_GROUP

# request field
NAME_MAXIMUM_LENGHTH = 50
ZIPCODE_PATTERN = '^[0-9]{5}(?:-[0-9]{4})?$'
EMAIL_PATTERN = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

# response fields
RESP_DATA = 'data'
RESP_STATUS = 'status'
RESP_MESSAGE = 'message'
RESP_ERROR = 'error'
RESP_METADATA = 'metadata'
RESP_RESPONSE = 'response'

MERCHANT_CONFIG_COLLECTION = 'MerchantConfig'

# Authorize.net
GATEWAY_AUTHORIZE_NET = 'Authorize.net'
AUTH_ONLY_TRANSACTION = 'authOnlyTransaction'
AUTH_CAPTURE_TRANSACTION = 'authCaptureTransaction'
AUTHORIZE_NET_APPROVAL_RESPONSE_CODE = 'I00001'
AUTHORIZE_NET_PENDING_RESPONSE_CODE = 'E00078'

# Heartland
GATEWAY_HEARTLAND = 'Heartland'

HEARTLAND_BOLLETTA_SOAP_URL = 'https://staging.heartlandpaymentservices.net/BillingDataManagement/v3/BillingDataManagementService.svc'              # noqa
HEARTLAND_BOLLETTA_WSDL_URL = 'https://staging.heartlandpaymentservices.net/BillingDataManagement/v3/BillingDataManagementService.svc?singlewsdl'   # noqa
HEARTLAND_BILL_TYPE = 'Citation Payment'

# http responses
RESPONSE_TRANSACTION_AUTHORIZATION = 'Transaction Authorization Executed.'
RESPONSE_PAYMENT = 'Payment Request Processed.'
RESPONSE_TRANSACTION_REPORT = 'Got Transaction Report'

# errors
ERR_TRANSACTION_AUTHORIZATION = 'Error Transaction Authorization'
ERR_PAYMENT = 'Error Payment'
ERR_TRANSACTION_REPORT = 'Error Transaction Report'

# gateway transaction status
TRANSACTION_APPROVAL = 'APPROVAL'
TRANSACTION_PENDING = 'PENDING'
TRANSACTION_FAILURE = 'FAILURE'

# valid credit card expiration year gap
EXPIRATION_YEAR_GAP = 5
