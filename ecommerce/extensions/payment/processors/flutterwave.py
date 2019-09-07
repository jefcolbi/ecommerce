""" Flutterwave payment processing. """
from __future__ import unicode_literals

import base64
import datetime
import json
import logging
import uuid
from decimal import Decimal

from django.conf import settings
from django.urls import reverse
from oscar.apps.payment.exceptions import GatewayError, TransactionDeclined, UserCancelled
from oscar.core.loading import get_class, get_model
from zeep import Client
from zeep.helpers import serialize_object
from zeep.wsse import UsernameToken

from ecommerce.core.constants import ISO_8601_FORMAT
from ecommerce.core.url_utils import get_ecommerce_url
from ecommerce.extensions.checkout.utils import get_receipt_page_url
from ecommerce.extensions.payment.constants import APPLE_PAY_CYBERSOURCE_CARD_TYPE_MAP, CYBERSOURCE_CARD_TYPE_MAP
from ecommerce.extensions.payment.exceptions import (
    AuthorizationError,
    DuplicateReferenceNumber,
    InvalidCybersourceDecision,
    InvalidSignatureError,
    PartialAuthorizationError,
    PCIViolation,
    ProcessorMisconfiguredError
)
from ecommerce.extensions.payment.helpers import sign
from ecommerce.extensions.payment.processors import (
    ApplePayMixin,
    BaseClientSidePaymentProcessor,
    HandledProcessorResponse
)
from ecommerce.extensions.payment.utils import clean_field_value

logger = logging.getLogger(__name__)

Order = get_model('order', 'Order')
OrderNumberGenerator = get_class('order.utils', 'OrderNumberGenerator')


class Flutterwave(BaseClientSidePaymentProcessor):
    """
    CyberSource Secure Acceptance Web/Mobile (February 2015)

    For reference, see
    http://apps.cybersource.com/library/documentation/dev_guides/Secure_Acceptance_WM/Secure_Acceptance_WM.pdf.
    """

    NAME = 'flutterwave'

    def __init__(self, site):
        """
        Constructs a new instance of the CyberSource processor.

        Raises:
            KeyError: If no settings configured for this payment processor
            AttributeError: If LANGUAGE_CODE setting is not set.
        """

        super(Flutterwave, self).__init__(site)
        configuration = self.configuration
        # FLWPUBK_TEST-fdbd68467800534095b5df4853773acd-X
        self.publishable_key = configuration.get("pub_key", None)
        # FLWSECK_TEST-f7df577f7e1f33600a9ef764d73332b1-X
        self.secret_key = configuration.get('secret_key', None)

    @property
    def cancel_url(self):
        return get_ecommerce_url(self.configuration['cancel_checkout_path'])

    @property
    def error_url(self):
        return get_ecommerce_url(self.configuration['error_path'])    

    @property
    def client_side_payment_url(self):
        return urljoin(get_ecommerce_url(), reverse('flutterwave:execute'))
    
    def get_transaction_parameters(self, basket, request=None, use_client_side_checkout=True, **kwargs):
        raise NotImplementedError('The Flutterwave payment processor does not support transaction parameters.')

    def handle_processor_response(self, response, basket=None):
        """
        Handle a response (i.e., "merchant notification") from CyberSource.

        Arguments:
            response (dict): Dictionary of parameters received from the payment processor.

        Keyword Arguments:
            basket (Basket): Basket being purchased via the payment processor.

        Raises:
            AuthorizationError: Authorization was declined.
            UserCancelled: Indicates the user cancelled payment.
            TransactionDeclined: Indicates the payment was declined by the processor.
            GatewayError: Indicates a general error on the part of the processor.
            InvalidCyberSourceDecision: Indicates an unknown decision value.
                Known values are ACCEPT, CANCEL, DECLINE, ERROR, REVIEW.
            PartialAuthorizationError: Indicates only a portion of the requested amount was authorized.

        Returns:
            HandledProcessorResponse
        """
        
        data = response['data']
        status = response['status']
        message = response['message']
        try:
            chargecode = response['data']['chargecode']
        except:
            chargecode = None
            
        if chargecode == "00" or chargecode == "0":
            pass
        else:
            logger.error("Transaction failed: response", str(response))
            raise TransactionDeclined

        currency = response['data']['currency']
        total = Decimal(response['data']['amount'])
        try:
            transaction_id = response['data']['txid']  # Error Notifications does not include a transaction id.
        except:
            transaction_id = None
        card_number = response['data']['card']['last4digits']
        card_type = response['data']['card']['brand']

        return HandledProcessorResponse(
            transaction_id=transaction_id,
            total=total,
            currency=currency,
            card_number=card_number,
            card_type=card_type
        )
    
    def issue_credit(self, order_number, basket, reference_number, amount, currency):
        raise NotImplementedError    

    
