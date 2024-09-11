from ...utils import logger, Obj
from ...models import PaymentRequest
from ...constants import GATEWAY_AUTHORIZE_NET, TRANSACTION_APPROVAL, \
                      TRANSACTION_FAILURE
from .authorize_net import credit_card_payment

import logging
import json
import unittest

logging.basicConfig(level=logging.INFO)


class AuthorizeNetTests(unittest.TestCase):
    """Unit Test for Authorize.net Gateway"""
    # def test_authorize_card_payment(self):
    #     """Authorize.net Gateway Authorize Card Payment Success Case"""
        # request = PaymentRequest(gateway=GATEWAY_AUTHORIZE_NET, amount='25.2',
        #                          card_number='4111111111111111',
        #                          exp_year='2027',
        #                          exp_month='12', cvc='123',
        #                          first_name='Michael', last_name='Jordan',
        #                          address='123 Test Street',
        #                          city='Test City', state='CA', zipcode='54611',
        #                          country='United States of America',
        #                          phone_number='+18004444444',
        #                          email_address='test@test.com',
        #                          reference_id='MerchantID-0001')
    #     request.check_request_validity()
    #     response = authorize_net.authorize_card_payment(request)
    #     self.assertNotEqual(None, response)
    #     resp = Obj(response)
    #     self.assertEqual(TRANSACTION_APPROVAL, resp.status)
    #     logger.info('[test_authorize_card_payment] ' +
    #                 json.dumps(response, default=vars))

    # def test_reporting(self):
    #     """Authorize.net Gateway Reporting Success Case"""
    #     items = reporting()
    #     self.assertNotEqual(None, items)
    #     logger.info('[test_reporting] ' + json.dumps(items, default=vars))

    # Credit Card Payment Success case
    def test_card_payment_success(self):
        """Authorize.net Gateway Credit Card Payment Success Case"""
        request = PaymentRequest(gateway=GATEWAY_AUTHORIZE_NET, amount='25.2',
                                 card_number='4111111111111111',
                                 exp_year='2027',
                                 exp_month='12', cvc='123',
                                 first_name='Michael', last_name='Jordan',
                                 address='123 Test Street',
                                 city='Test City', state='CA', zipcode='54611',
                                 country='United States of America',
                                 phone_number='+18004444444',
                                 email_address='test@test.com',
                                 reference_id='MerchantID-0001')
        request.check_request_validity()
        response = credit_card_payment(request)
        self.assertNotEqual(None, response)
        resp = Obj(response)
        self.assertEqual(TRANSACTION_APPROVAL, resp.status)
        logger.info('[test_charge_credit_card_success] ' +
                    json.dumps(response, default=vars))

    # Credit Card Payment Failure cases
    # Duplicated request Error - If the user send same request continuously,
    #                            it will be failed by duplicated request
    # def test_card_payment_failure1(self):
    #     """Authorize.net Gateway Credit Card Payment Failure Case:"""
    #     """Duplicate Request"""
        # request = PaymentRequest(gateway=GATEWAY_AUTHORIZE_NET, amount='25.2',
        #                          card_number='4111111111111111',
        #                          exp_year='2027',
        #                          exp_month='12', cvc='123',
        #                          first_name='Michael', last_name='Jordan',
        #                          address='123 Test Street',
        #                          city='Test City', state='CA', zipcode='54611',
        #                          country='United States of America',
        #                          phone_number='+18004444444',
        #                          email_address='test@test.com',
        #                          reference_id='MerchantID-0001')
    #     response = charge_credit_card(request)
    #     self.assertNotEqual(None, response)
    #     resp = Obj(response)
    #     self.assertNotEqual(TRANSACTION_FAILURE, resp.status)
    #     logger.info(json.dumps(response, default=vars))

    def test_card_payment_failure_invalid_amount(self):
        """Authorize.net Gateway Credit Card Payment Failure Case:"""
        """Invalid Amount - Less Than 1"""
        request = PaymentRequest(gateway=GATEWAY_AUTHORIZE_NET, amount='0',
                                 card_number='4111111111111111',
                                 exp_year='2027',
                                 exp_month='12', cvc='123',
                                 first_name='Michael', last_name='Jordan',
                                 address='123 Test Street',
                                 city='Test City', state='CA', zipcode='54611',
                                 country='United States of America',
                                 phone_number='+18004444444',
                                 email_address='test@test.com',
                                 reference_id='MerchantID-0001')
        response = credit_card_payment(request)
        self.assertNotEqual(None, response)
        resp = Obj(response)
        self.assertEqual(TRANSACTION_FAILURE, resp.status)
        logger.info('[test_charge_credit_card_failure case: '
                    'invalid amount - less than 1] ' +
                    json.dumps(response, default=vars))

    def test_card_payment_failure_invalid_cardnumber(self):
        """Authorize.net Gateway Credit Card Payment Failure Case:"""
        """Invalid Credit Card Number - Not A Correct Card Number Format"""
        request = PaymentRequest(gateway=GATEWAY_AUTHORIZE_NET, amount='25.2',
                                 card_number='411111111111111',
                                 exp_year='2027',
                                 exp_month='12', cvc='123',
                                 first_name='Michael', last_name='Jordan',
                                 address='123 Test Street',
                                 city='Test City', state='CA', zipcode='54611',
                                 country='United States of America',
                                 phone_number='+18004444444',
                                 email_address='test@test.com',
                                 reference_id='MerchantID-0001')
        response = credit_card_payment(request)
        self.assertNotEqual(None, response)
        resp = Obj(response)
        self.assertEqual(TRANSACTION_FAILURE, resp.status)
        logger.info('[test_charge_credit_card_failure case: '
                    'invalid credit card number - '
                    'not a correct card number format] ' +
                    json.dumps(response, default=vars))

    def test_card_payment_failure_invalid_expiration_year_1(self):
        """Authorize.net Gateway Credit Card Payment Failure Case:"""
        """Invalid Expiration Year - Not A Year Number"""
        request = PaymentRequest(gateway=GATEWAY_AUTHORIZE_NET, amount='25.2',
                                 card_number='4111111111111111',
                                 exp_year='A',
                                 exp_month='12', cvc='123',
                                 first_name='Michael', last_name='Jordan',
                                 address='123 Test Street',
                                 city='Test City', state='CA', zipcode='54611',
                                 country='United States of America',
                                 phone_number='+18004444444',
                                 email_address='test@test.com',
                                 reference_id='MerchantID-0001')
        response = credit_card_payment(request)
        self.assertNotEqual(None, response)
        resp = Obj(response)
        self.assertEqual(TRANSACTION_FAILURE, resp.status)
        logger.info('[test_charge_credit_card_failure case: '
                    'invalid expiration year - not a year number] ' +
                    json.dumps(response, default=vars))

    def test_card_payment_failure_invalid_expiration_year_2(self):
        """Authorize.net Gateway Credit Card Payment Failure Case:"""
        """Invalid Expiration Year - Less Than This Year"""
        request = PaymentRequest(gateway=GATEWAY_AUTHORIZE_NET, amount='25.2',
                                 card_number='4111111111111111',
                                 exp_year='2021',
                                 exp_month='12', cvc='123',
                                 first_name='Michael', last_name='Jordan',
                                 address='123 Test Street',
                                 city='Test City', state='CA', zipcode='54611',
                                 country='United States of America',
                                 phone_number='+18004444444',
                                 email_address='test@test.com',
                                 reference_id='MerchantID-0001')
        response = credit_card_payment(request)
        self.assertNotEqual(None, response)
        resp = Obj(response)
        self.assertEqual(TRANSACTION_FAILURE, resp.status)
        logger.info('[test_charge_credit_card_failure case: '
                    'invalid expiration year - less than this year] ' +
                    json.dumps(response, default=vars))

    def test_card_payment_failure_invalid_expiration_month_1(self):
        """Authorize.net Gateway Credit Card Payment Failure Case:"""
        """Invalid Expiration Month - Not A Month Number"""
        request = PaymentRequest(gateway=GATEWAY_AUTHORIZE_NET, amount='25.2',
                                 card_number='4111111111111111',
                                 exp_year='2027',
                                 exp_month='A', cvc='123',
                                 first_name='Michael', last_name='Jordan',
                                 address='123 Test Street',
                                 city='Test City', state='CA', zipcode='54611',
                                 country='United States of America',
                                 phone_number='+18004444444',
                                 email_address='test@test.com',
                                 reference_id='MerchantID-0001')
        response = credit_card_payment(request)
        self.assertNotEqual(None, response)
        resp = Obj(response)
        self.assertEqual(TRANSACTION_FAILURE, resp.status)
        logger.info('[test_charge_credit_card_failure case: '
                    'invalid expiration month - not a month number] ' +
                    json.dumps(response, default=vars))

    def test_card_payment_failure_invalid_expiration_month_2(self):
        """Authorize.net Gateway Credit Card Payment Failure Case:"""
        """Invalid Expiration Month - Greater Than 12"""
        request = PaymentRequest(gateway=GATEWAY_AUTHORIZE_NET, amount='25.2',
                                 card_number='4111111111111111',
                                 exp_year='2027',
                                 exp_month='13', cvc='123',
                                 first_name='Michael', last_name='Jordan',
                                 address='123 Test Street',
                                 city='Test City', state='CA', zipcode='54611',
                                 country='United States of America',
                                 phone_number='+18004444444',
                                 email_address='test@test.com',
                                 reference_id='MerchantID-0001')
        response = credit_card_payment(request)
        self.assertNotEqual(None, response)
        resp = Obj(response)
        self.assertEqual(TRANSACTION_FAILURE, resp.status)
        logger.info('[test_charge_credit_card_failure case: '
                    'invalid expiration month - greater than 12] ' +
                    json.dumps(response, default=vars))

    def test_card_payment_failure_invalid_expiration_month_3(self):
        """Authorize.net Gateway Credit Card Payment Failure Case:"""
        """Invalid Expiration Month - Less Than 1"""
        request = PaymentRequest(gateway=GATEWAY_AUTHORIZE_NET, amount='25.2',
                                 card_number='4111111111111111',
                                 exp_year='2027',
                                 exp_month='0', cvc='123',
                                 first_name='Michael', last_name='Jordan',
                                 address='123 Test Street',
                                 city='Test City', state='CA', zipcode='54611',
                                 country='United States of America',
                                 phone_number='+18004444444',
                                 email_address='test@test.com',
                                 reference_id='MerchantID-0001')
        response = credit_card_payment(request)
        self.assertNotEqual(None, response)
        resp = Obj(response)
        self.assertEqual(TRANSACTION_FAILURE, resp.status)
        logger.info('[test_charge_credit_card_failure case: '
                    'invalid expiration month - less than 1] ' +
                    json.dumps(response, default=vars))


if __name__ == '__main__':
    unittest.main()
