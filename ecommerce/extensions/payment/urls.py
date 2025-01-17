from __future__ import absolute_import

from django.conf.urls import include, url

from ecommerce.extensions.payment.views import PaymentFailedView, SDNFailure, cybersource, paypal, stripe, flutterwave

CYBERSOURCE_APPLE_PAY_URLS = [
    url(r'^authorize/$', cybersource.CybersourceApplePayAuthorizationView.as_view(), name='authorize'),
    url(r'^start-session/$', cybersource.ApplePayStartSessionView.as_view(), name='start_session'),
]
CYBERSOURCE_URLS = [
    url(r'^apple-pay/', include(CYBERSOURCE_APPLE_PAY_URLS, namespace='apple_pay')),
    url(r'^redirect/$', cybersource.CybersourceInterstitialView.as_view(), name='redirect'),
    url(r'^submit/$', cybersource.CybersourceSubmitView.as_view(), name='submit'),
    url(r'^api-submit/$', cybersource.CybersourceSubmitAPIView.as_view(), name='api_submit'),
]

PAYPAL_URLS = [
    url(r'^execute/$', paypal.PaypalPaymentExecutionView.as_view(), name='execute'),
    url(r'^profiles/$', paypal.PaypalProfileAdminView.as_view(), name='profiles'),
]

SDN_URLS = [
    url(r'^failure/$', SDNFailure.as_view(), name='failure'),
]

STRIPE_URLS = [
    url(r'^submit/$', stripe.StripeSubmitView.as_view(), name='submit'),
]

FLUTTERWAVE_URLS = [
    url(r'^execute/$', flutterwave.FlutterwavePaymentExecutionView.as_view(), name='execute'),
]

urlpatterns = [
    url(r'^cybersource/', include(CYBERSOURCE_URLS, namespace='cybersource')),
    url(r'^error/$', PaymentFailedView.as_view(), name='payment_error'),
    url(r'^paypal/', include(PAYPAL_URLS, namespace='paypal')),
    url(r'^sdn/', include(SDN_URLS, namespace='sdn')),
    url(r'^stripe/', include(STRIPE_URLS, namespace='stripe')),
    url(r'^flutterwave/', include(FLUTTERWAVE_URLS, namespace='flutterwave')),
]
