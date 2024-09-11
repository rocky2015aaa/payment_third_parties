# authorise.net_POC

- Contract

https://documenter.getpostman.com/view/861554/2s83zjqhXB

1. Authorize.net payment request
```
curl --location --request POST 'http://localhost:8000/payment-gateway/payment' \
--header 'Content-Type: application/json' \
--data-raw '{
  "gateway": "Authorize.net",             // has validation
  "amount": "1.26",                       // has validation
  "card_number": "4111111111111111",      // has validation
  "exp_year": "2027",                     // has validation
  "exp_month": "12",                      // has validation
  "cvc": "123",                           // has validation
  "first_name": "Test",                   // has validation
  "last_name": "Person",                  // has validation
  "address": "123 Test Street",           
  "city": "City",
  "state": "AK",                          // has validation
  "zipcode": "36811",                     // has validation
  "country": "United States of America",  // For USA, only Full name activates state validation
  "phone_number": "+18004444444",         // has validation
  "email_address": "test@test.com",       // has validation
  "reference_id": "Merchant-001"
}'
```
2. Authorize.net payment response    
For reference_id in response, the server takes refTransId from payment_metadata.
https://github.com/ParkLoyaltyEngineering/authorise.net_POC/blob/main/app/gateway_vendors/authorize_net/authorize_net.py#L222    
But authorize.net returns null. 
- Success
```
{
    "data": {
        "status": "APPROVAL",
        "reference_id": "NDZ8CEIVXJRLFW7XEA8H773",
        "payment_metadata": {
            "refId": "Merchant-001",
            "messages": {
                "resultCode": "Ok",
                "message": {
                    "code": "I00001",
                    "text": "Successful."
                }
            },
            "transactionResponse": {
                "responseCode": "1",
                "authCode": "QSTGDZ",
                "avsResultCode": "Y",
                "cvvResultCode": "P",
                "cavvResultCode": "2",
                "transId": "60202150639",
                "refTransID": null,
                "transHash": null,
                "testRequest": "0",
                "accountNumber": "XXXX1111",
                "accountType": "Visa",
                "messages": {
                    "message": {
                        "code": "1",
                        "description": "This transaction has been approved."
                    }
                },
                "transHashSha2": "3E2F7172A13D4D56EC6377AE62ACCCEF4C11FA595A5CCC5AC762F8E19FC63BEAFB4F78BA32255361DD9244997AE914FBFEE4BB28E26ABC026EF99CAE3157F1A7",
                "networkTransId": "NDZ8CEIVXJRLFW7XEA8H773"
            }
        }
    },
    "status": true,
    "message": "Payment Request Processed."
}
```
- Failure
```
{
    "data": {
        "status": "FAILURE",
        "error_messages": [
            "The credit card number is invalid."
        ],
        "payment_metadata": {
            "refId": "Merchant-001",
            "messages": {
                "resultCode": "Error",
                "message": {
                    "code": "E00027",
                    "text": "The transaction was unsuccessful."
                }
            },
            "transactionResponse": {
                "responseCode": "3",
                "authCode": null,
                "avsResultCode": "P",
                "cvvResultCode": null,
                "cavvResultCode": null,
                "transId": "0",
                "refTransID": null,
                "transHash": null,
                "testRequest": "0",
                "accountNumber": "XXXX1111",
                "accountType": null,
                "errors": {
                    "error": {
                        "errorCode": "6",
                        "errorText": "The credit card number is invalid."
                    }
                },
                "transHashSha2": "33E85DE08F068E7B5C70D65FD5BC0D8F417C44A3328EF895CC8388428C7359C7603174DD805C01006A302219086B1DFBFF4A64F4C1248DC12BC62015EC2B346E"
            }
        }
    },
    "status": true,
    "message": "Payment Request Processed."
}
```
3. Heartland payment requestHeartland does not have reference_id for the request.
```
curl --location --request POST 'http://localhost:8000/payment-gateway/payment' \
--header 'Content-Type: application/json' \
--data-raw '{
  "gateway": "Heartland",                  // has validation
  "amount": "1.26",                        // has validation
  "card_number": "4111111111111111",       // has validation
  "exp_year": "2027",                      // has validation
  "exp_month": "12",                       // has validation
  "cvc": "123",                            // has validation
  "first_name": "Test",                    // has validation
  "last_name": "Person",                   // has validation
  "address": "123 Test Street",
  "city": "City",
  "state": "AK",                           // has validation
  "zipcode": "36811",                      // has validation
  "country": "United States of America",   // For USA, only Full name activates state validation
  "phone_number": "+18004444444",          // has validation
  "email_address": "test@test.com",        // has validation
  "site_id": "2d689158-dcca-4e49-94f3-5ef82439228e",
  "citation_ids": ["54444","12345","34345"]
}'
```
4. Heartland payment response
For reference_id in response, the server takes reference_number from payment_metadata.https://github.com/ParkLoyaltyEngineering/authorise.net_POC/blob/main/app/gateway_vendors/heartland/heartland.py#L134
- Success
```
{
    "data": {
        "status": "APPROVAL",
        "reference_id": "1789253148",
        "payment_metadata": {
            "Messages": null,
            "isSuccessful": true,
            "FileContent": null,
            "FileName": null,
            "Authorizations": {
                "Authorization": [
                    {
                        "AccountExpirationMonth": 12,
                        "AccountExpirationYear": 2027,
                        "AddToBatchReferenceNumber": "1789253148",
                        "Amount": 1.26,
                        "AuthCode": "19023A",
                        "AuthorizationType": "Base",
                        "Gateway": "POSGateway",
                        "GatewayBatchID": null,
                        "GatewayDescription": "POSGateway",
                        "MaskedAccountNumber": "1111",
                        "MaskedRoutingNumber": "    ",
                        "PaymentMethod": "VisaCredit",
                        "ReferenceAuthorizationID": null,
                        "ReferenceNumber": "1789253148"
                    }
                ]
            },
            "Transaction": {
                "Amount": 1.26,
                "FeeAmount": 0.0,
                "MerchantInvoiceNumber": null,
                "MerchantPONumber": null,
                "MerchantTransactionDescription": null,
                "MerchantTransactionID": null,
                "PayorAddress": "123 Test Street",
                "PayorCity": "City",
                "PayorCountry": "US",
                "PayorEmailAddress": "test@test.com",
                "PayorFirstName": "Test",
                "PayorLastName": "Person",
                "PayorMiddleName": null,
                "PayorPhoneNumber": "7986123456",
                "PayorPostalCode": "36811",
                "PayorState": "CA",
                "ReferenceTransactionID": null,
                "TransactionDate": "2022-10-09T01:37:42.766841+00:00"
            },
            "Transaction_ID": 9463032
        }
    },
    "status": true,
    "message": "Payment Request Processed."
}
```
- Failure
```
{
    "data": {
        "status": "FAILURE",
        "error_messages": [
            "The ClearText Credit Card CardNumber is invalid for ClearTextCardToCharge 1.",
            "The ClearText Credit Card ExpirationMonth is missing for ClearTextCardToCharge 1."
        ],
        "payment_metadata": {
            "Messages": {
                "Message": [
                    {
                        "Code": 301,
                        "Level": "Unknown",
                        "MessageDescription": "The ClearText Credit Card CardNumber is invalid for ClearTextCardToCharge 1."
                    },
                    {
                        "Code": 303,
                        "Level": "Unknown",
                        "MessageDescription": "The ClearText Credit Card ExpirationMonth is missing for ClearTextCardToCharge 1."
                    }
                ]
            },
            "isSuccessful": false,
            "FileContent": null,
            "FileName": null,
            "Authorizations": null,
            "Transaction": null,
            "Transaction_ID": 0
        }
    },
    "status": true,
    "message": "Payment Request Processed."
}
```
5. General Request Validation Error
```
{
    "error": "Error Payment",
    "status": false,
    "message": "['card_number 411111111111111 is not valid', 'exp_month 0 must be in [1, 12]']"
}
```
