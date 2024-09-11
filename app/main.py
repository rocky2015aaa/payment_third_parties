from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .utils import logger, DecimalEncoder
from .models import PaymentRequest
from .handlers import authorize_credit_card, pay_credit_card, tx_report
from .constants import ROUTE_GROUP, ROUTE_AUTHORIZATION_TRANSACTION, \
                      ROUTE_PAYMENT, ROUTE_REPORT, \
                      ERR_TRANSACTION_AUTHORIZATION, ERR_PAYMENT, \
                      ERR_TRANSACTION_REPORT, \
                      RESPONSE_TRANSACTION_AUTHORIZATION, \
                      RESPONSE_PAYMENT, RESPONSE_TRANSACTION_REPORT

import json
import logging
from . import responses

logging.basicConfig(level=logging.INFO)

app = FastAPI()
origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/')
async def root():
    return responses.ResponseModelV2('Park Loyalty', 'Park Loyalty API')


@app.get('/%s' % ROUTE_GROUP)
async def root():
    return responses.ResponseModelV2('Park Loyalty',
                                     'Park Loyalty Payment gateway API')


@app.post(ROUTE_AUTHORIZATION_TRANSACTION)
async def authorization_transaction(request: PaymentRequest):
    try:
        request.check_request_validity()
        result = authorize_credit_card[request.gateway](request)
        logger.info(ROUTE_AUTHORIZATION_TRANSACTION + ' request: ' +
                    json.dumps(request, default=vars))
        logger.info(ROUTE_AUTHORIZATION_TRANSACTION + ' result: ' +
                    json.dumps(result, default=vars))
        return responses.ResponseModelV2(result,
                                         RESPONSE_TRANSACTION_AUTHORIZATION)
    except Exception as e:
        logger.info(ROUTE_AUTHORIZATION_TRANSACTION + ' request: ' +
                    json.dumps(request, default=vars))
        logger.info(ROUTE_AUTHORIZATION_TRANSACTION + ' result: ' +
                    e.__class__.__name__ + ', ' + str(e))
        return responses.ErrorResponseModel(ERR_TRANSACTION_AUTHORIZATION,
                                            False, str(e))


@app.post(ROUTE_PAYMENT)
async def payment(request: PaymentRequest):
    try:
        request.check_request_validity()
        result = pay_credit_card[request.gateway](request)
        logger.info(ROUTE_PAYMENT + ' request: ' +
                    json.dumps(request, default=vars))
        logger.info(ROUTE_PAYMENT + ' result: ' +
                    json.dumps(result, cls=DecimalEncoder, default=str))
        return responses.ResponseModelV2(result, RESPONSE_PAYMENT)
    except Exception as e:
        logger.info(ROUTE_PAYMENT + ' request: ' +
                    json.dumps(request, default=vars))
        logger.info(ROUTE_PAYMENT + ' result: ' +
                    e.__class__.__name__ + ', ' + str(e))
        return responses.ErrorResponseModel(ERR_PAYMENT,  False, str(e))


@app.get(ROUTE_REPORT)
async def report(gateway_name):
    try:
        result = tx_report[gateway_name]()
        logger.info(ROUTE_REPORT + ' result list: ' + str(len(result)))
        return responses.ResponseModelV2(result, RESPONSE_TRANSACTION_REPORT)
    except Exception as e:
        logger.info(ROUTE_REPORT + ' result: ' +
                    e.__class__.__name__ + ', ' + str(e))
        return responses.ErrorResponseModel(ERR_TRANSACTION_REPORT,
                                            False, str(e))
