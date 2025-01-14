from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _
from oscar.core.loading import get_model

from ecommerce.journals.benefits import JournalBundleAbsoluteDiscountBenefit, JournalBundlePercentageDiscountBenefit

Benefit = get_model('offer', 'Benefit')

BENEFIT_MAP = {
    Benefit.PERCENTAGE: JournalBundlePercentageDiscountBenefit,
    Benefit.FIXED: JournalBundleAbsoluteDiscountBenefit,
}

BENEFIT_TYPE_CHOICES = (
    (Benefit.PERCENTAGE, _('Percentage')),
    (Benefit.FIXED, _('Absolute')),
)
