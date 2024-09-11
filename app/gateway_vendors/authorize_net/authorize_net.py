from authorizenet import apicontractsv1
from authorizenet.apicontrollers import createTransactionController, \
                                        getTransactionListController
from app.models import PaymentRequest, PaymentResponse
from app.utils import logger, Obj
from app.exporter import API_LOGIN_ID, TRANSACTION_KEY
from app.constants import AUTHORIZE_NET_APPROVAL_RESPONSE_CODE, \
                      AUTHORIZE_NET_PENDING_RESPONSE_CODE, \
                      AUTH_ONLY_TRANSACTION, \
                      AUTH_CAPTURE_TRANSACTION, TRANSACTION_APPROVAL, \
                      TRANSACTION_PENDING, TRANSACTION_FAILURE

import logging
import re

logging.basicConfig(level=logging.INFO)


def authorize_card_payment(request: PaymentRequest) -> dict:
    """Authorize a credit card (without actually charging it)"""
    create_transaction_request = get_transaction_request(request,
                                                         AUTH_ONLY_TRANSACTION)

    # Create the controller
    create_transaction_controller = createTransactionController(
        create_transaction_request)
    create_transaction_controller.execute()

    response = create_transaction_controller.getresponse()

    if response is not None:
        # Check to see if the API request was successfully received
        # and acted upon
        if response.messages.resultCode == 'Ok':
            # Since the API request was successful,
            # look for a transaction response
            # and parse it to display the results of authorizing the card
            if hasattr(response.transactionResponse, 'messages') is True:
                logger.info('Successfully created transaction with Transaction ID: %s' % response.transactionResponse.transId)  # noqa
                logger.info('Transaction Response Code: %s' % response.transactionResponse.responseCode)                        # noqa
                logger.info('Message Code: %s' % response.transactionResponse.messages.message[0].code)                         # noqa
                logger.info('Description: %s' % response.transactionResponse.messages.message[0].description)                   # noqa
            else:
                logger.info('Failed Transaction.')
                if hasattr(response.transactionResponse, 'errors') is True:
                    logger.info('Error Code:  %s' % str(response.transactionResponse.errors.error[0].errorCode))                # noqa
                    logger.info('Error message: %s' % response.transactionResponse.errors.error[0].errorText)                   # noqa
        # Or, print errors if the API request wasn't successful
        else:
            logger.info('Failed Transaction.')
            if hasattr(response, 'transactionResponse') is True and \
               hasattr(response.transactionResponse, 'errors') is True:
                logger.info('Error Code: %s' % str(response.transactionResponse.errors.error[0].errorCode))                     # noqa
                logger.info('Error message: %s' % response.transactionResponse.errors.error[0].errorText)                       # noqa
            else:
                logger.info('Error Code: %s' % response.messages.message[0]['code'].text)                                       # noqa
                logger.info('Error message: %s' % response.messages.message[0]['text'].text)                                    # noqa
    else:
        logger.info('Null Response.')

    # return xml_to_dict(getAuthorizeNetPaymentResponse(response))
    return get_authorize_net_payment_response(response).__dict__


def credit_card_payment(request: PaymentRequest) -> dict:
    """Charge a credit card"""
    create_transaction_request = get_transaction_request(request, AUTH_CAPTURE_TRANSACTION)                                      # noqa

    # Create the controller
    create_transaction_controller = createTransactionController(
        create_transaction_request)
    create_transaction_controller.execute()

    response = create_transaction_controller.getresponse()

    if response is not None:
        # Check to see if the API request was successfully received
        # and acted upon
        if response.messages.resultCode == 'Ok':
            # Since the API request was successful,
            # look for a transaction response
            # and parse it to display the results of authorizing the card
            if hasattr(response.transactionResponse, 'messages') is True:
                logger.info('Successfully created transaction with Transaction ID: %s' % response.transactionResponse.transId)  # noqa
                logger.info('Transaction Response Code: %s' % response.transactionResponse.responseCode)                        # noqa
                logger.info('Message Code: %s' % response.transactionResponse.messages.message[0].code)                         # noqa
                logger.info('Description: %s' % response.transactionResponse.messages.message[0].description)                   # noqa
            else:
                logger.info('Failed Transaction.')
                if hasattr(response.transactionResponse, 'errors') is True:
                    logger.info('Error Code:  %s' % str(response.transactionResponse.errors.error[0].errorCode))                # noqa
                    logger.info('Error message: %s' % response.transactionResponse.errors.error[0].errorText)                   # noqa
        # Or, logger.log errors if the API request wasn't successful
        else:
            logger.info('Failed Transaction.')
            if hasattr(response, 'transactionResponse') is True and hasattr(
                    response.transactionResponse, 'errors') is True:
                logger.info('Error Code: %s' % str(response.transactionResponse.errors.error[0].errorCode))                     # noqa
                logger.info('Error message: %s' % response.transactionResponse.errors.error[0].errorText)                       # noqa
            else:
                logger.info('Error Code: %s' % response.messages.message[0]['code'].text)                                       # noqa
                logger.info('Error message: %s' % response.messages.message[0]['text'].text)                                    # noqa
    else:
        logger.info('Null Response.')

    return get_authorize_net_payment_response(response).__dict__
    # return xml_to_dict(response)


def reporting() -> dict:
    """Get transaction list"""
    merchant_auth = apicontractsv1.merchantAuthenticationType()
    merchant_auth.name = API_LOGIN_ID
    merchant_auth.transactionKey = TRANSACTION_KEY

    # set sorting parameters
    sorting = apicontractsv1.TransactionListSorting()
    sorting.orderBy = apicontractsv1.TransactionListOrderFieldEnum.id
    sorting.orderDescending = True

    # set paging and offset parameters
    paging = apicontractsv1.Paging()
    # Paging limit can be up to 1000 for this request
    paging.limit = 20
    paging.offset = 1

    transaction_list_request = apicontractsv1.getTransactionListRequest()
    transaction_list_request.merchantAuthentication = merchant_auth
    # transactionListRequest.refId = 'Sample'
    transaction_list_request.batchId = '4606008'
    transaction_list_request.sorting = sorting
    transaction_list_request.paging = paging

    transaction_list_controller = getTransactionListController(transaction_list_request)                                        # noqa
    transaction_list_controller.execute()

    # Work on the response
    response = transaction_list_controller.getresponse()

    if response is not None:
        if response.messages.resultCode == apicontractsv1.messageTypeEnum.Ok:
            if hasattr(response, 'transactions'):
                logger.info('Successfully retrieved transaction list.')
                if response.messages is not None:
                    logger.info('Message Code: %s' % response.messages.message[0]['code'].text)                                 # noqa
                    logger.info('Message Text: %s' % response.messages.message[0]['text'].text)                                 # noqa
                    logger.info('Total Number In Results: %s' % response.totalNumInResultSet)                                   # noqa
                    logger.info()
                for transaction in response.transactions.transaction:
                    logger.info('Transaction Id: %s' % transaction.transId)
                    logger.info('Transaction Status: %s' % transaction.transactionStatus)                                       # noqa
                    if hasattr(transaction, 'accountType'):
                        logger.info('Account Type: %s' % transaction.accountType)                                               # noqa
                    logger.info('Settle Amount: %.2f' % transaction.settleAmount)                                               # noqa
                    if hasattr(transaction, 'profile'):
                        logger.info('Customer Profile ID: %s' % transaction.profile.customerProfileId)                          # noqa
                    logger.info()
            else:
                if response.messages is not None:
                    logger.info('Failed to get transaction list.')
                    logger.info('Code: %s' % (response.messages.message[0]['code'].text))                                       # noqa
                    logger.info('Text: %s' % (response.messages.message[0]['text'].text))                                       # noqa
        else:
            if response.messages is not None:
                logger.info('Failed to get transaction list.')
                logger.info('Code: %s' % (response.messages.message[0]['code'].text))                                           # noqa
                logger.info('Text: %s' % (response.messages.message[0]['text'].text))                                           # noqa
    else:
        logger.info('Error. No response received.')

    return xml_to_dict(response)


def get_transaction_request(request: PaymentRequest, transactionType: str) -> object:                                           # noqa
    """Create a transaction request"""
    # Create a merchantAuthenticationType object with authentication details
    # retrieved from the constants file
    merchant_auth = apicontractsv1.merchantAuthenticationType()
    merchant_auth.name = API_LOGIN_ID
    merchant_auth.transactionKey = TRANSACTION_KEY

    # Create the payment data for a credit card
    credit_card = apicontractsv1.creditCardType()
    credit_card.cardNumber = request.card_number                                                                                # noqa e.g. '4111111111111111'
    credit_card.expirationDate = request.exp_year + '-' + request.exp_month                                                     # noqa e.g. '2026-12'
    credit_card.cardCode = request.cvc                                                                                          # noqa e.g. '123'

    # Add the payment data to a paymentType object
    payment = apicontractsv1.paymentType()
    payment.creditCard = credit_card

    # Set the customer's Bill To address
    customer_address = apicontractsv1.customerAddressType()
    customer_address.firstName = request.first_name
    customer_address.lastName = request.last_name
    customer_address.address = request.address
    customer_address.city = request.city
    customer_address.state = request.state
    customer_address.zip = request.zipcode
    customer_address.country = request.country

    # Set the customer's identifying information
    customer_data = apicontractsv1.customerDataType()
    customer_data.type = "individual"
    customer_data.email = request.email_address

    # Create a transactionRequestType object
    # and add the previous objects to it.
    transaction_request = apicontractsv1.transactionRequestType()
    transaction_request.transactionType = transactionType
    transaction_request.amount = request.amount
    transaction_request.payment = payment

    # Assemble the complete transaction request
    create_transaction_request = apicontractsv1.createTransactionRequest()
    create_transaction_request.merchantAuthentication = merchant_auth
    create_transaction_request.refId = request.reference_id                                                                     # noqa e.g. 'MerchantID-0001'
    create_transaction_request.transactionRequest = transaction_request

    return create_transaction_request


def xml_to_dict(element) -> dict:
    """Convert xml object to dict"""
    ret = {}
    if element.getchildren() == []:
        return element.text
    else:
        for elem in element.getchildren():
            subdict = xml_to_dict(elem)
            ret[re.sub('{.*}', '', elem.tag)] = subdict
    return ret


def get_authorize_net_payment_response(resp) -> object:
    """Create and return a response"""
    resp_obj = Obj(xml_to_dict(resp))

    response = PaymentResponse()
    if resp_obj.messages.message.code == AUTHORIZE_NET_APPROVAL_RESPONSE_CODE:
        response.status = TRANSACTION_APPROVAL
        response.reference_id = resp_obj.transactionResponse.networkTransId
    elif resp_obj.messages.message.code == AUTHORIZE_NET_PENDING_RESPONSE_CODE:
        response.status = TRANSACTION_PENDING
        response.reference_id = resp_obj.transactionResponse.networkTransId
    else:
        response.status = TRANSACTION_FAILURE
        response.error_messages = [resp_obj.transactionResponse.errors.error.errorText]  # noqa authorize.net returns only one error message even if it gets more than one invalid input

    response.payment_metadata = resp_obj

    return response
