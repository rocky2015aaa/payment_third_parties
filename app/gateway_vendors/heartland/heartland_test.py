from ...utils import logger, Obj, DecimalEncoder
from ...models import PaymentRequest
from ...constants import GATEWAY_HEARTLAND, TRANSACTION_APPROVAL, \
                      TRANSACTION_FAILURE
from .heartland import credit_card_payment

import logging
import json
import unittest

logging.basicConfig(level=logging.INFO)


class HeartlandTests(unittest.TestCase):
    """Unit Test for Heartland Gateway"""
    # Credit Card Payment Success case
    def test_credit_card_payment_success(self):
        """Heartland Gateway Credit Card Payment Success Case"""
        request = PaymentRequest(gateway=GATEWAY_HEARTLAND, amount='25.2',
                                 card_number='4111111111111111',
                                 exp_year='2027',
                                 exp_month='12', cvc='123',
                                 first_name='Michael', last_name='Jordan',
                                 address='123 Test Street',
                                 city='Test City', state='CA', zipcode='54611',
                                 country='United States of America',
                                 phone_number='+18004444444',
                                 email_address='test@test.com',
                                 site_id='a2a5d53d-1dd5-4dfb-8672-bde84e4dbd3f',                     # noqa
                                 citation_ids=['54444','12345','34345'])
        request.check_request_validity()
        response = credit_card_payment(request)
        self.assertNotEqual(None, response)
        resp = Obj(response)
        self.assertEqual(TRANSACTION_APPROVAL, resp.status)
        logger.info('[test_credit_card_payment_success case] ' +
                    json.dumps(response, cls=DecimalEncoder, default=str))

    # Credit Card Payment Failure cases
    def test_credit_card_payment_failure_invalid_amount(self):
        """Heartland Gateway Credit Card Payment Failure Case: """
        """Invalid Amount - Less Than 1"""
        request = PaymentRequest(gateway=GATEWAY_HEARTLAND, amount='0',
                                 card_number='4111111111111111',
                                 exp_year='2027',
                                 exp_month='12', cvc='123',
                                 first_name='Michael', last_name='Jordan',
                                 address='123 Test Street',
                                 city='Test City', state='CA', zipcode='54611',
                                 country='United States of America',
                                 phone_number='+18004444444',
                                 email_address='test@test.com',
                                 site_id='a2a5d53d-1dd5-4dfb-8672-bde84e4dbd3f',                     # noqa
                                 citation_ids=['54444','12345','34345'])
        response = credit_card_payment(request)
        self.assertNotEqual(None, response)
        resp = Obj(response)
        self.assertEqual(TRANSACTION_FAILURE, resp.status)
        logger.info('[test_credit_card_payment_failure case: '
                    'invalid amount - less than 1] ' +
                    json.dumps(response, cls=DecimalEncoder, default=str))

    def test_credit_card_payment_failure_invalid_cardnumber(self):
        """Heartland Gateway Credit Card Payment Failure Case: """
        """Invalid Credit Card Number - Not A Correct Card Number Format"""
        request = PaymentRequest(gateway=GATEWAY_HEARTLAND, amount='25.2',
                                 card_number='411111111111111',
                                 exp_year='2027',
                                 exp_month='12', cvc='123',
                                 first_name='Michael', last_name='Jordan',
                                 address='123 Test Street',
                                 city='Test City', state='CA', zipcode='54611',
                                 country='United States of America',
                                 phone_number='+18004444444',
                                 email_address='test@test.com',
                                 site_id='a2a5d53d-1dd5-4dfb-8672-bde84e4dbd3f',                     # noqa
                                 citation_ids=['54444','12345','34345'])
        response = credit_card_payment(request)
        self.assertNotEqual(None, response)
        resp = Obj(response)
        self.assertEqual(TRANSACTION_FAILURE, resp.status)
        logger.info('[test_credit_card_payment_failure case: '
                    'invalid credit card number - '
                    'not a correct card number format] ' +
                    json.dumps(response, cls=DecimalEncoder, default=str))

    def test_credit_card_payment_failure_invalid_expiration_month_1(self):
        """Heartland Gateway Credit Card Payment Failure Case: """
        """Invalid Expiration Month - Greater Than 12"""
        request = PaymentRequest(gateway=GATEWAY_HEARTLAND, amount='25.2',
                                 card_number='4111111111111111',
                                 exp_year='2027',
                                 exp_month='13', cvc='123',
                                 first_name='Michael', last_name='Jordan',
                                 address='123 Test Street',
                                 city='Test City', state='CA', zipcode='54611',
                                 country='United States of America',
                                 phone_number='+18004444444',
                                 email_address='test@test.com',
                                 site_id='a2a5d53d-1dd5-4dfb-8672-bde84e4dbd3f',                     # noqa
                                 citation_ids=['54444','12345','34345'])
        response = credit_card_payment(request)
        self.assertNotEqual(None, response)
        resp = Obj(response)
        self.assertEqual(TRANSACTION_FAILURE, resp.status)
        logger.info('[test_credit_card_payment_failure case: '
                    'invalid expiration month - greater than 12] ' +
                    json.dumps(response, cls=DecimalEncoder, default=str))

    def test_credit_card_payment_failure_invalid_expiration_month_2(self):
        """Heartland Gateway Credit Card Payment Failure Case: """
        """Invalid Expiration Month - Less Than 1"""
        request = PaymentRequest(gateway=GATEWAY_HEARTLAND, amount='25.2',
                                 card_number='4111111111111111',
                                 exp_year='2027',
                                 exp_month='0', cvc='123',
                                 first_name='Michael', last_name='Jordan',
                                 address='123 Test Street',
                                 city='Test City', state='CA', zipcode='54611',
                                 country='United States of America',
                                 phone_number='+18004444444',
                                 email_address='test@test.com',
                                 site_id='a2a5d53d-1dd5-4dfb-8672-bde84e4dbd3f',                     # noqa
                                 citation_ids=['54444','12345','34345'])
        response = credit_card_payment(request)
        self.assertNotEqual(None, response)
        resp = Obj(response)
        self.assertEqual(TRANSACTION_FAILURE, resp.status)
        logger.info('[test_credit_card_payment_failure case: '
                    'invalid expiration month - less than 1] ' +
                    json.dumps(response, cls=DecimalEncoder, default=str))

    def test_credit_card_payment_invalid_phone_number(self):
        """Heartland Gateway Credit Card Payment Failure Case: """
        """Invalid Phone Number - Wrong Phone Number"""
        request = PaymentRequest(gateway=GATEWAY_HEARTLAND, amount='25.2',
                                 card_number='4111111111111111',
                                 exp_year='2027',
                                 exp_month='12', cvc='123',
                                 first_name='Michael', last_name='Jordan',
                                 address='123 Test Street',
                                 city='Test City', state='CA', zipcode='54611',
                                 country='United States of America',
                                 phone_number='+180044444441',
                                 email_address='test@test.com',
                                 site_id='a2a5d53d-1dd5-4dfb-8672-bde84e4dbd3f',                     # noqa
                                 citation_ids=['54444','12345','34345'])
        response = credit_card_payment(request)
        self.assertNotEqual(None, response)
        resp = Obj(response)
        self.assertEqual(TRANSACTION_FAILURE, resp.status)
        logger.info('[test_credit_card_payment_failure case: '
                    'invalid phone number - wrong phone number] ' +
                    json.dumps(response, cls=DecimalEncoder, default=str))

    def test_credit_card_failure_invalid_email(self):
        """Heartland Gateway Credit Card Payment Failure Case: """
        """Invalid Email - Wrong Email"""
        request = PaymentRequest(gateway=GATEWAY_HEARTLAND, amount='25.2',
                                 card_number='4111111111111111',
                                 exp_year='2027',
                                 exp_month='12', cvc='123',
                                 first_name='Michael', last_name='Jordan',
                                 address='123 Test Street',
                                 city='Test City', state='CA', zipcode='54611',
                                 country='United States of America',
                                 phone_number='+18004444444',
                                 email_address='test-test.com',
                                 site_id='a2a5d53d-1dd5-4dfb-8672-bde84e4dbd3f',                     # noqa
                                 citation_ids=['54444','12345','34345'])
        response = credit_card_payment(request)
        self.assertNotEqual(None, response)
        resp = Obj(response)
        self.assertEqual(TRANSACTION_FAILURE, resp.status)
        logger.info('[test_credit_card_payment_failure case: '
                    'invalid email - wrong email] ' +
                    json.dumps(response, cls=DecimalEncoder, default=str))


if __name__ == '__main__':
    unittest.main()
