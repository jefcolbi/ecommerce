""" JournalViewSet """
from __future__ import absolute_import

from oscar.core.loading import get_model
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from ecommerce.journals.api.serializers import JournalProductSerializer, JournalProductUpdateSerializer
from ecommerce.journals.constants import JOURNAL_PRODUCT_CLASS_NAME

Product = get_model('catalogue', 'Product')


class JournalProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows journals to be viewed or edited.
    """
    # this does lookup based on UUID value of productattributevalue table
    lookup_field = 'attribute_values__value_text'
    queryset = Product.objects.filter(product_class__name=JOURNAL_PRODUCT_CLASS_NAME)
    serializer_class = JournalProductSerializer
    permission_classes = (IsAdminUser,)

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.request and hasattr(self.request, 'method'):
            if self.request.method == 'PATCH' or self.request.method == 'PUT':
                serializer_class = JournalProductUpdateSerializer

        return serializer_class
