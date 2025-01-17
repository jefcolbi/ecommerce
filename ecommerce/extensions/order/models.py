from __future__ import absolute_import

from django.db import models
from django.utils.translation import ugettext_lazy as _
from oscar.apps.order.abstract_models import AbstractLine, AbstractOrder, AbstractPaymentEvent
from simple_history.models import HistoricalRecords

from ecommerce.extensions.fulfillment.status import ORDER


class Order(AbstractOrder):
    partner = models.ForeignKey('partner.Partner', null=True, blank=True)
    history = HistoricalRecords()

    @property
    def is_fulfillable(self):
        """Returns a boolean indicating if order can be fulfilled."""
        return self.status in (ORDER.OPEN, ORDER.FULFILLMENT_ERROR)

    @property
    def contains_coupon(self):
        """ Return a boolean if the order contains a Coupon. """
        return any(line.product.is_coupon_product for line in self.basket.all_lines())

    @property
    def is_journal_order(self):
        """ Return a boolean if the order contains Journal product. """
        return any(line.product.is_journal_product for line in self.basket.all_lines()) if self.basket else False


class Line(AbstractLine):
    history = HistoricalRecords()


class PaymentEvent(AbstractPaymentEvent):
    processor_name = models.CharField(_('Payment Processor'), max_length=32, blank=True, null=True)


# If two models with the same name are declared within an app, Django will only use the first one.
# noinspection PyUnresolvedReferences
from oscar.apps.order.models import *  # noqa isort:skip pylint: disable=wildcard-import,unused-wildcard-import,wrong-import-position,wrong-import-order,ungrouped-imports
