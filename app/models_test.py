from .models import PaymentRequest, InvalidGatewayRequestError
from .constants import GATEWAY_AUTHORIZE_NET, GATEWAY_HEARTLAND

import unittest


class PaymentRequestValidationTests(unittest.TestCase):
    # Payment Request Validation Success cases
    def test_payment_request_validation_success_1(self):
        """PaymentRequest Validation Success Case: Authorize.net GateWay"""
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

    def test_payment_request_validation_success_2(self):
        """PaymentRequest Validation Success Case: Heartland Gateway"""
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
                                 site_id='2d689158-dcca-4e49-94f3-5ef82439228e',                     # noqa
                                 citation_ids=['54444', '12345', '34345'])
        request.check_request_validity()

    # Payment Request Validation Failure cases
    def test_payment_request_validation_failure_invalid_gateway_name(self):
        """PaymentRequest Validation Failure Case: Invalid GateWay Name"""
        request = PaymentRequest(gateway='Other gateway', amount='25.2',
                                 card_number='4111111111111111',
                                 exp_year='2027',
                                 exp_month='12', cvc='123',
                                 first_name='Michael', last_name='Jordan',
                                 address='123 Test Street',
                                 city='Test City', state='CA', zipcode='54611',
                                 country='United States of America',
                                 phone_number='+18004444444',
                                 email_address='test@test.com',
                                 site_id='2d689158-dcca-4e49-94f3-5ef82439228e',                      # noqa
                                 citation_ids=['54444', '12345', '34345'])
        self.assertRaises(InvalidGatewayRequestError,
                          request.check_request_validity)

    def test_payment_request_validation_failure_missing_reference_id_for_authorize_net(self):         # noqa
        """PaymentRequest Validation Failure Case:"""
        """Authorize.net GateWay - Missing Reference ID"""
        request = PaymentRequest(gateway=GATEWAY_AUTHORIZE_NET, amount='25.2',
                                 card_number='4111111111111111',
                                 exp_year='2027',
                                 exp_month='12', cvc='123',
                                 first_name='Michael', last_name='Jordan',
                                 address='123 Test Street',
                                 city='Test City', state='CA', zipcode='54611',
                                 country='United States of America',
                                 phone_number='+18004444444',
                                 email_address='test@test.com')
        self.assertRaises(InvalidGatewayRequestError,
                          request.check_request_validity)

    def test_payment_request_validation_failure_missing_site_id_for_heartland(self):                  # noqa
        """PaymentRequest Validation Failure Case:"""
        """Heartland GateWay - Missing Site ID"""
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
                                 citation_ids=['54444', '12345', '34345'])
        self.assertRaises(InvalidGatewayRequestError,
                          request.check_request_validity)

    def test_payment_request_validation_failure_missing_citation_ids_for_heartland(self):                 # noqa
        """PaymentRequest Validation Failure Case:"""
        """Heartland GateWay - Missing Citation Number"""
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
                                 site_id='2d689158-dcca-4e49-94f3-5ef82439228e')                     # noqa
        self.assertRaises(InvalidGatewayRequestError,
                          request.check_request_validity)

    def test_payment_request_validation_failure_invalid_amount_1(self):
        """PaymentRequest Validation Failure Case:"""
        """Invalid Amount - Not A Number"""
        request = PaymentRequest(gateway=GATEWAY_HEARTLAND, amount='A',
                                 card_number='4111111111111111',
                                 exp_year='2027',
                                 exp_month='12', cvc='123',
                                 first_name='Michael', last_name='Jordan',
                                 address='123 Test Street',
                                 city='Test City', state='CA', zipcode='54611',
                                 country='United States of America',
                                 phone_number='+18004444444',
                                 email_address='test@test.com',
                                 site_id='2d689158-dcca-4e49-94f3-5ef82439228e',                     # noqa
                                 citation_ids=['54444', '12345', '34345'])
        self.assertRaises(ValueError, request.check_request_validity)

    def test_payment_request_validation_failure_invalid_amount_2(self):
        """PaymentRequest Validation Failure Case:"""
        """Invalid Amount - less than 1"""
        request = PaymentRequest(gateway=GATEWAY_HEARTLAND, amount='-1.2',
                                 card_number='4111111111111111',
                                 exp_year='2027',
                                 exp_month='12', cvc='123',
                                 first_name='Michael', last_name='Jordan',
                                 address='123 Test Street',
                                 city='Test City', state='CA', zipcode='54611',
                                 country='United States of America',
                                 phone_number='+18004444444',
                                 email_address='test@test.com',
                                 site_id='2d689158-dcca-4e49-94f3-5ef82439228e',                     # noqa
                                 citation_ids=['54444', '12345', '34345'])
        self.assertRaises(InvalidGatewayRequestError,
                          request.check_request_validity)

    def test_payment_request_validation_failure_invalid_cardnumber_1(self):
        """PaymentRequest Validation Failure Case:"""
        """Invalid Credit Card Number - Not A Card Number"""
        request = PaymentRequest(gateway=GATEWAY_HEARTLAND, amount='25.2',
                                 card_number='A', exp_year='2027',
                                 exp_month='12', cvc='123',
                                 first_name='Michael', last_name='Jordan',
                                 address='123 Test Street',
                                 city='Test City', state='CA', zipcode='54611',
                                 country='United States of America',
                                 phone_number='+18004444444',
                                 email_address='test@test.com',
                                 site_id='2d689158-dcca-4e49-94f3-5ef82439228e',                     # noqa
                                 citation_ids=['54444', '12345', '34345'])
        self.assertRaises(ValueError, request.check_request_validity)

    def test_payment_request_validation_failure_invalid_cardnumber_2(self):
        """PaymentRequest Validation Failure Case:"""
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
                                 site_id='2d689158-dcca-4e49-94f3-5ef82439228e',                      # noqa
                                 citation_ids=['54444', '12345', '34345'])
        self.assertRaises(InvalidGatewayRequestError,
                          request.check_request_validity)

    def test_payment_request_validation_failure_invalid_expiration_year_1(self):                      # noqa
        """PaymentRequest Validation Failure Case:"""
        """Invalid Expiration Year - Not A Year Number"""
        request = PaymentRequest(gateway=GATEWAY_HEARTLAND, amount='25.2',
                                 card_number='4111111111111111',
                                 exp_year='A',
                                 exp_month='12', cvc='123',
                                 first_name='Michael', last_name='Jordan',
                                 address='123 Test Street',
                                 city='Test City', state='CA', zipcode='54611',
                                 country='United States of America',
                                 phone_number='+18004444444',
                                 email_address='test@test.com',
                                 site_id='2d689158-dcca-4e49-94f3-5ef82439228e',                      # noqa
                                 citation_ids=['54444', '12345', '34345'])
        self.assertRaises(ValueError, request.check_request_validity)

    def test_payment_request_validation_failure_invalid_expiration_year_2(self):                      # noqa
        """PaymentRequest Validation Failure Case:"""
        """Invalid Expiration Year - 5 Years Greater Than This Year"""
        request = PaymentRequest(gateway=GATEWAY_HEARTLAND, amount='25.2',
                                 card_number='4111111111111111',
                                 exp_year='2029',
                                 exp_month='12', cvc='123',
                                 first_name='Michael', last_name='Jordan',
                                 address='123 Test Street',
                                 city='Test City', state='CA', zipcode='54611',
                                 country='United States of America',
                                 phone_number='+18004444444',
                                 email_address='test@test.com',
                                 site_id='2d689158-dcca-4e49-94f3-5ef82439228e',                      # noqa
                                 citation_ids=['54444', '12345', '34345'])
        self.assertRaises(InvalidGatewayRequestError,
                          request.check_request_validity)

    def test_payment_request_validation_failure_invalid_expiration_year_3(self):                      # noqa
        """PaymentRequest Validation Failure Case:"""
        """Invalid Expiration Year - Less Than This Year"""
        request = PaymentRequest(gateway=GATEWAY_HEARTLAND, amount='25.2',
                                 card_number='4111111111111111',
                                 exp_year='2021',
                                 exp_month='12', cvc='123',
                                 first_name='Michael', last_name='Jordan',
                                 address='123 Test Street',
                                 city='Test City', state='CA', zipcode='54611',
                                 country='United States of America',
                                 phone_number='+18004444444',
                                 email_address='test@test.com',
                                 site_id='2d689158-dcca-4e49-94f3-5ef82439228e',                      # noqa
                                 citation_ids=['54444', '12345', '34345'])
        self.assertRaises(InvalidGatewayRequestError,
                          request.check_request_validity)

    def test_payment_request_validation_failure_invalid_expiration_month_1(self):                     # noqa
        """PaymentRequest Validation Failure Case:"""
        """Invalid Expiration Month - Not A Month Number"""
        request = PaymentRequest(gateway=GATEWAY_HEARTLAND, amount='25.2',
                                 card_number='4111111111111111',
                                 exp_year='2027',
                                 exp_month='A', cvc='123',
                                 first_name='Michael', last_name='Jordan',
                                 address='123 Test Street',
                                 city='Test City', state='CA', zipcode='54611',
                                 country='United States of America',
                                 phone_number='+18004444444',
                                 email_address='test@test.com',
                                 site_id='2d689158-dcca-4e49-94f3-5ef82439228e',                      # noqa
                                 citation_ids=['54444', '12345', '34345'])
        self.assertRaises(ValueError, request.check_request_validity)

    def test_payment_request_validation_failure_invalid_expiration_month_2(self):                     # noqa
        """PaymentRequest Validation Failure Case:"""
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
                                 site_id='2d689158-dcca-4e49-94f3-5ef82439228e',                      # noqa
                                 citation_ids=['54444', '12345', '34345'])
        self.assertRaises(InvalidGatewayRequestError,
                          request.check_request_validity)

    def test_payment_request_validation_failure_invalid_expiration_month_3(self):                     # noqa
        """PaymentRequest Validation Failure Case:"""
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
                                 site_id='2d689158-dcca-4e49-94f3-5ef82439228e',                      # noqa
                                 citation_ids=['54444', '12345', '34345'])
        self.assertRaises(InvalidGatewayRequestError,
                          request.check_request_validity)

    def test_payment_request_validation_failure_invalid_expiration_month_4(self):                     # noqa
        """PaymentRequest Validation Failure Case:"""
        """Invalid Expiration Month - Already Expired Date"""
        request = PaymentRequest(gateway=GATEWAY_HEARTLAND, amount='25.2',
                                 card_number='4111111111111111',
                                 exp_year='2022',
                                 exp_month='9', cvc='123',
                                 first_name='Michael', last_name='Jordan',
                                 address='123 Test Street',
                                 city='Test City', state='CA', zipcode='54611',
                                 country='United States of America',
                                 phone_number='+18004444444',
                                 email_address='test@test.com',
                                 site_id='2d689158-dcca-4e49-94f3-5ef82439228e',                     # noqa
                                 citation_ids=['54444', '12345', '34345'])
        self.assertRaises(InvalidGatewayRequestError,
                          request.check_request_validity)

    def test_payment_request_validation_failure_invalid_cvc_1(self):
        """PaymentRequest Validation Failure Case:"""
        """Invalid CVC - Not A Number"""
        request = PaymentRequest(gateway=GATEWAY_HEARTLAND, amount='25.2',
                                 card_number='4111111111111111',
                                 exp_year='2027',
                                 exp_month='12', cvc='A',
                                 first_name='Michael', last_name='Jordan',
                                 address='123 Test Street',
                                 city='Test City', state='CA', zipcode='54611',
                                 country='United States of America',
                                 phone_number='+18004444444',
                                 email_address='test@test.com',
                                 site_id='2d689158-dcca-4e49-94f3-5ef82439228e',                     # noqa
                                 citation_ids=['54444', '12345', '34345'])
        self.assertRaises(InvalidGatewayRequestError,
                          request.check_request_validity)

    def test_payment_request_validation_failure_invalid_cvc_2(self):
        """PaymentRequest Validation Failure Case:"""
        """Invalid CVC - Not A CVC Format"""
        request = PaymentRequest(gateway=GATEWAY_HEARTLAND, amount='25.2',
                                 card_number='4111111111111111',
                                 exp_year='2027',
                                 exp_month='12', cvc='12',
                                 first_name='Michael', last_name='Jordan',
                                 address='123 Test Street',
                                 city='Test City', state='CA', zipcode='54611',
                                 country='United States of America',
                                 phone_number='+18004444444',
                                 email_address='test@test.com',
                                 site_id='2d689158-dcca-4e49-94f3-5ef82439228e',                     # noqa
                                 citation_ids=['54444', '12345', '34345'])
        self.assertRaises(InvalidGatewayRequestError,
                          request.check_request_validity)

    def test_payment_request_validation_failure_invalid_first_name(self):
        """PaymentRequest Validation Failure Case:"""
        """Invalid First Name - Too Long First Name"""
        request = PaymentRequest(gateway=GATEWAY_HEARTLAND, amount='25.2',
                                 card_number='4111111111111111',
                                 exp_year='2027',
                                 exp_month='12', cvc='123',
                                 first_name='Thisisalongtesttextthisisalongtesttextthisisalongtesttext',  # noqa
                                 last_name='Jordan',
                                 address='123 Test Street',
                                 city='Test City', state='CA', zipcode='54611',
                                 country='United States of America',
                                 phone_number='+18004444444',
                                 email_address='test@test.com',
                                 site_id='2d689158-dcca-4e49-94f3-5ef82439228e',                     # noqa
                                 citation_ids=['54444', '12345', '34345'])
        self.assertRaises(InvalidGatewayRequestError,
                          request.check_request_validity)

    def test_payment_request_validation_failure_invalid_last_name(self):
        """PaymentRequest Validation Failure Case:"""
        """Invalid Last Name - Too Long Last Name"""
        request = PaymentRequest(gateway=GATEWAY_HEARTLAND, amount='25.2',
                                 card_number='4111111111111111',
                                 exp_year='2027',
                                 exp_month='12', cvc='123',
                                 first_name='Michael',
                                 last_name='Thisisalongtesttextthisisalongtesttextthisisalongtesttext',  # noqa
                                 address='123 Test Street',
                                 city='Test City', state='CA', zipcode='54611',
                                 country='United States of America',
                                 phone_number='+18004444444',
                                 email_address='test@test.com',
                                 site_id='2d689158-dcca-4e49-94f3-5ef82439228e',                     # noqa
                                 citation_ids=['54444', '12345', '34345'])
        self.assertRaises(InvalidGatewayRequestError,
                          request.check_request_validity)

    def test_payment_request_validation_failure_invalid_state_name(self):
        """PaymentRequest Validation Failure Case:"""
        """Invalid State Name - Not A State Name"""
        request = PaymentRequest(gateway=GATEWAY_HEARTLAND, amount='25.2',
                                 card_number='4111111111111111',
                                 exp_year='2027',
                                 exp_month='12', cvc='123',
                                 first_name='Michael', last_name='Jordan',
                                 address='123 Test Street',
                                 city='Test City', state='QQ', zipcode='54611',
                                 country='United States of America',
                                 phone_number='+18004444444',
                                 email_address='test@test.com',
                                 site_id='2d689158-dcca-4e49-94f3-5ef82439228e',                     # noqa
                                 citation_ids=['54444', '12345', '34345'])
        self.assertRaises(InvalidGatewayRequestError,
                          request.check_request_validity)

    def test_payment_request_validation_failure_invalid_zip_code(self):
        """PaymentRequest Validation Failure Case:"""
        """Invalid Zip Code - Wrong Zip Code"""
        request = PaymentRequest(gateway=GATEWAY_HEARTLAND, amount='25.2',
                                 card_number='4111111111111111',
                                 exp_year='2027',
                                 exp_month='12', cvc='123',
                                 first_name='Michael', last_name='Jordan',
                                 address='123 Test Street',
                                 city='Test City', state='CA', zipcode='54',
                                 country='United States of America',
                                 phone_number='+18004444444',
                                 email_address='test@test.com',
                                 site_id='2d689158-dcca-4e49-94f3-5ef82439228e',                     # noqa
                                 citation_ids=['54444', '12345', '34345'])
        self.assertRaises(InvalidGatewayRequestError,
                          request.check_request_validity)

    def test_payment_request_validation_failure_invalid_phone_number(self):
        """PaymentRequest Validation Failure Case:"""
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
                                 site_id='2d689158-dcca-4e49-94f3-5ef82439228e',                     # noqa
                                 citation_ids=['54444', '12345', '34345'])
        self.assertRaises(InvalidGatewayRequestError,
                          request.check_request_validity)

    def test_payment_request_validation_failure_invalid_email(self):
        """PaymentRequest Validation Failure Case:"""
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
                                 site_id='2d689158-dcca-4e49-94f3-5ef82439228e',                     # noqa
                                 citation_ids=['54444', '12345', '34345'])
        self.assertRaises(InvalidGatewayRequestError,
                          request.check_request_validity)


if __name__ == '__main__':
    unittest.main()
