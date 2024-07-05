from django.urls import path
from .views import PaymentAPI,CreatePaymentIntentView, MakePayment,SaveStripeInfo

urlpatterns = [
    path('make_payment/', PaymentAPI.as_view(), name='make_payment'),
    path('payment/', CreatePaymentIntentView.as_view(), name='payment'),
    path('testpay/', MakePayment.as_view(), name='testpayment'),
    path('stripe-user/', SaveStripeInfo.as_view(), name='stripe-user')
]