from django.urls import path
from .views import PaymentAPI,CreatePaymentIntentView

urlpatterns = [
    path('make_payment/', PaymentAPI.as_view(), name='make_payment'),
    path('payment/', CreatePaymentIntentView.as_view(), name='payment')
]