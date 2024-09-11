from pydantic import BaseModel
from .gateway_vendors.vendor_list import gateway_vendor_list
from .constants import NAME_MAXIMUM_LENGHTH, ZIPCODE_PATTERN, \
                      EMAIL_PATTERN, GATEWAY_AUTHORIZE_NET, \
                      GATEWAY_HEARTLAND, EXPIRATION_YEAR_GAP
from .utils import logger
from datetime import date
from typing import Optional

import phonenumbers
import re
import logging
import sys
sys.path.append('.')

logging.basicConfig(level=logging.INFO)

us_states = {'AK': None, 'AL': None, 'AR': None, 'AZ': None, 'CA': None,
             'CO': None, 'CT': None, 'DC': None, 'DE': None, 'FL': None,
             'GA': None, 'HI': None, 'IA': None, 'ID': None, 'IL': None,
             'IN': None, 'KS': None, 'KY': None, 'LA': None, 'MA': None,
             'MD': None, 'ME': None, 'MI': None, 'MN': None, 'MO': None,
             'MS': None, 'MT': None, 'NC': None, 'ND': None, 'NE': None,
             'NH': None, 'NJ': None, 'NM': None, 'NV': None, 'NY': None,
             'OH': None, 'OK': None, 'OR': None, 'PA': None, 'RI': None,
             'SC': None, 'SD': None, 'TN': None, 'TX': None, 'UT': None,
             'VA': None, 'VT': None, 'WA': None, 'WI': None, 'WV': None,
             'WY': None}


class PaymentRequest(BaseModel):
    """Payment gateway request"""
    gateway: str
    amount: str
    card_number: str
    exp_year: str
    exp_month: str
    cvc: str

    # Credit Card Holder Information
    first_name: str
    last_name: str
    address: str
    city: str
    state: str
    zipcode: str
    country: str
    phone_number: str
    email_address: str

    reference_id: Optional[str]
    site_id: Optional[str]
    citation_ids: Optional[list]

    def check_request_validity(self):
        """Check if request data is valid"""
        msg_list = []
        if self.gateway not in gateway_vendor_list:                                 # noqa gateway name must be Authorize.net or Heartland
            msg = 'gateway name ' + self.gateway + \
                  ' is not a valid gateway name'
            logger.info(msg)
            msg_list.append(msg)
        if self.gateway == GATEWAY_AUTHORIZE_NET and self.reference_id is None:     # noqa Authorize.net request must have reference_id
            msg = self.gateway + ' needs reference id'
            logger.info(msg)
            msg_list.append(msg)
        if self.gateway == GATEWAY_HEARTLAND and self.site_id is None:              # noqa Heartland request must have site_id
            msg = self.gateway + ' needs site id'
            logger.info(msg)
            msg_list.append(msg)
        if self.gateway == GATEWAY_HEARTLAND and self.citation_ids is None:      # noqa Heartland request must have citation_ids
            msg = self.gateway + ' needs citation ids'
            logger.info(msg)
            msg_list.append(msg)
        if float(self.amount) <= 0:                                                 # noqa amount must be bigger than 0
            msg = 'amount ' + self.amount + ' must be bigger than 0'
            logger.info(msg)
            msg_list.append(msg)
        if luhn_checksum(self.card_number) != 0:                                    # noqa check if card number is valid
            msg = 'card_number '+self.card_number+' is not valid'
            logger.info(msg)
            msg_list.append(msg)
        if int(self.exp_year) < date.today().year or \
            int(self.exp_year) > date.today().year+EXPIRATION_YEAR_GAP:             # noqa expiration year range must be in in [this year,  this year + 5](e.g. [2022(this year), 2027])
            msg = 'exp_year ' + self.exp_year + ' must be in [' + \
                  str(date.today().year) + ',' + \
                  str(date.today().year + EXPIRATION_YEAR_GAP)+']'
            logger.info(msg)
            msg_list.append(msg)
        if int(self.exp_month) > 12 or int(self.exp_month) < 1:                     # noqa expiration month must be in 1 to 12
            msg = 'exp_month ' + self.exp_month + ' must be in [1, 12]'
            logger.info(msg)
            msg_list.append(msg)
        if int(self.exp_year) == date.today().year and int(self.exp_month) < date.today().month:   # noqa expiration month of this year must be more than this month(must not be already expired)
            msg = 'exp_month ' + self.exp_month + ' in exp year ' + \
                  self.exp_year + ' must be more than ' + \
                  str(date.today().month) + \
                  ' (expiration date must not be already expired)'
            logger.info(msg)
            msg_list.append(msg)
        if is_valid_CVV_number(self.cvc) is False:                                  # noqa check if card cvc number is valid
            msg = 'cvc ' + self.cvc + ' is not valid'
            logger.info(msg)
            msg_list.append(msg)
        if len(self.first_name) > NAME_MAXIMUM_LENGHTH:                             # noqa first name length should not be less than 50
            msg = 'The letter length of ' + self.first_name + \
                  ' is longger than ' + str(NAME_MAXIMUM_LENGHTH)
            logger.info(msg)
            msg_list.append(msg)
        if len(self.last_name) > NAME_MAXIMUM_LENGHTH:                              # noqa last name length should not be less than 50
            msg = 'The letter length of ' + self.last_name + \
                  ' is longger than ' + str(NAME_MAXIMUM_LENGHTH)
            logger.info(msg)
            msg_list.append(msg)
        if re.match(ZIPCODE_PATTERN, self.zipcode) == None:                         # noqa check if card cvc number is valid
            msg = 'zip code ' + self.zipcode + ' is invalid'
            logger.info(msg)
            msg_list.append(msg)
        if self.country == 'United States of America':                              # noqa check if US state name is valid
            if self.state not in us_states:
                msg = 'states name is invalid'
                logger.info(msg)
                msg_list.append(msg)
        if phonenumbers.is_valid_number(phonenumbers.parse(self.phone_number)) == False:  # noqa check if phone number format is valid
            msg = 'phone number ' + self.phone_number + ' is invalid'
            logger.info(msg)
            msg_list.append(msg)
        if re.match(EMAIL_PATTERN, self.email_address) == None:                     # noqa check if email format is valid
            msg = 'email ' + self.email_address + ' is invalid'
            logger.info(msg)
            msg_list.append(msg)
        if len(msg_list) > 0:
            raise InvalidGatewayRequestError(msg_list)


class PaymentResponse():
    """Payment gateway response"""
    status: str
    reference_id: str
    error_messages: list()
    payment_metadata: object


class InvalidGatewayRequestError(Exception):
    """Exception raised for errors in the gateway request.

    Attributes:
        message -- explanation of the error
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def luhn_checksum(card_number):
    """check if card number is valid."""
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = 0
    checksum += sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d*2))
    return checksum % 10


def is_valid_CVV_number(str):
    """Regex to check valid CVV number."""
    regex = '^[0-9]{3,4}$'

    # Compile the ReGex
    p = re.compile(regex)

    # If the string is empty
    # return false
    if (str is None):
        return False

    # Return if the string
    # matched the ReGex
    if (re.search(p, str)):
        return True
    else:
        return False
