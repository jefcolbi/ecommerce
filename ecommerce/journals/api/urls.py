"""
Root API URLs.

All API URLs should be versioned, so urlpatterns should only
contain namespaces for the active versions of the API.
"""
from __future__ import absolute_import

from django.conf.urls import include, url

urlpatterns = [
    url(r'^v1/', include('ecommerce.journals.api.v1.urls', namespace='v1')),
]
