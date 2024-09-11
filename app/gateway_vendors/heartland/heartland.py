from suds.client import Client
from datetime import datetime
from app.database import get_mongo_client
from app.utils import logger, Obj, recursive_dict
from app.models import PaymentRequest, PaymentResponse
from app.constants import TRANSACTION_APPROVAL, TRANSACTION_FAILURE, \
                      HEARTLAND_BOLLETTA_WSDL_URL, \
                      HEARTLAND_BOLLETTA_SOAP_URL, HEARTLAND_BILL_TYPE, \
                      MERCHANT_CONFIG_COLLECTION, GATEWAY_HEARTLAND, \
                      HEARTLAND_BOLLETTA_API_USERNAME, \
                      HEARTLAND_BOLLETTA_API_PASSWORD, \
                      HEARTLAND_BDMS_MERCHANT_NAME

import logging
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
logging.basicConfig(level=logging.INFO)


def credit_card_payment(request: PaymentRequest) -> dict:
    """Charge a credit card"""
    db_instance = get_mongo_client()[request.site_id]
    collection = db_instance[MERCHANT_CONFIG_COLLECTION]
    doc = collection.find_one({'gate_way_name': GATEWAY_HEARTLAND})
    if doc is None:
        raise Exception('No document has gate_way_name "%s"' % GATEWAY_HEARTLAND)
    client = Client(url=HEARTLAND_BOLLETTA_WSDL_URL,
                    location=HEARTLAND_BOLLETTA_SOAP_URL)
    make_payment_request = client.factory.create('ns0:MakePaymentRequest')
    make_payment_request.Credential = {
        'ApplicationID': '3',
        'Password': doc[HEARTLAND_BOLLETTA_API_PASSWORD],
        'UserName': doc[HEARTLAND_BOLLETTA_API_USERNAME],
        'MerchantName': doc[HEARTLAND_BDMS_MERCHANT_NAME]
    }
    billtransaction = client.factory.create('ns0:BillTransaction')
    billtransaction.BillType = HEARTLAND_BILL_TYPE
    billtransaction.ID1 = ','.join(request.citation_ids)
    billtransaction.AmountToApplyToBill = request.amount
    make_payment_request.BillTransactions = {
        'BillTransaction': billtransaction
    }
    clearTextCardToCharge = client.factory.create('ns0:ClearTextCardToCharge')
    clearTextCardToCharge.Amount = request.amount
    clearTextCardToCharge.CardProcessingMethod = 'Credit'
    clearTextCardToCharge.ExpectedFeeAmount = '0.0'
    cardHolderData = client.factory.create('ns2:CardHolderData')
    cardHolderData.Address = request.address
    cardHolderData.City = request.city
    cardHolderData.Email = request.email_address
    cardHolderData.FirstName = request.first_name
    cardHolderData.LastName = request.last_name
    cardHolderData.Phone = request.phone_number
    cardHolderData.State = request.state
    cardHolderData.Zip = request.zipcode
    clearTextCardToCharge.ClearTextCreditCard = {
        'CardHolderData': cardHolderData,
        'CardNumber': request.card_number,
        'ExpirationMonth': request.exp_month,
        'ExpirationYear': request.exp_year,
        'VerificationCode': request.cvc
    }
    make_payment_request.ClearTextCreditCardsToCharge = {
        'ClearTextCardToCharge': clearTextCardToCharge
    }
    make_payment_request.IncludeReceiptInResponse = 'true'
    make_payment_request.IsRecurringPayment = 'false'
    make_payment_request.Language = 'NotProvided'
    make_payment_request.Transaction = {
        'Amount': request.amount,
        'FeeAmount': '0.0',
        'PayorAddress': request.address,
        'PayorCity': request.city,
        'PayorCountry': request.country,
        'PayorEmailAddress': request.email_address,
        'PayorFirstName': request.first_name,
        'PayorLastName': request.last_name,
        'PayorPhoneNumber': request.phone_number,
        'PayorPostalCode': request.zipcode,
        'PayorState': request.state,
        'TransactionDate': datetime.today().strftime("%Y-%m-%dT%X.%fZ")
    }
    logger.info(make_payment_request)

    response = recursive_dict(client.service.MakeBlindPayment(make_payment_request))  # noqa
    logger.info('response: '+str(response))

    return get_heartland_payment_response(response).__dict__


def get_heartland_payment_response(resp) -> PaymentResponse:
    """Create and return a response"""
    response_message = Obj(resp)
    payment_response = PaymentResponse()

    if response_message.isSuccessful:
        payment_response.status = TRANSACTION_APPROVAL
        payment_response.reference_id = str(Obj(response_message.Authorizations.Authorization[0]).ReferenceNumber)  # noqa reference number
    else:
        # Heartland has no pending response
        # https://cert.api2.heartlandportico.com/Gateway/PorticoDevGuide/build/PorticoDeveloperGuide/Issuer%20Response%20Codes.html
        payment_response.status = TRANSACTION_FAILURE
        payment_response.error_messages = []
        for message in response_message.Messages.Message:
            payment_response.error_messages.append(Obj(message).MessageDescription)  # noqa

    payment_response.payment_metadata = resp

    return payment_response
