from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CardInformationSerializer
from rest_framework import status
import stripe
from django.conf import settings


stripe.api_key = settings.STRIPE_SECRET_KEY


class CreatePaymentIntentView(APIView):
    def post(self, request):
        try:
            # Create a PaymentIntent
            amount = request.data.get('amount')
            currency = request.data.get('currency')
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency=currency,
                automatic_payment_methods={
                    'enabled': True,
                },
            )
            return Response({'client_secret': intent.client_secret})
        except Exception as e:
            return Response({'error': str(e)}, status=400)


class PaymentAPI(APIView):
    serializer_class = CardInformationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        print('request data\n\n', request.data)
        print('serializer data\n\n', serializer)

        if not serializer.is_valid():
            print('Serializer errors:', serializer.errors)
            response = {'errors': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST}
            return Response(response)

        data_dict = serializer.data
        stripe.api_key =settings.STRIPE_SECRET_KEY
        response = self.stripe_card_payment(data_dict=data_dict)

        return Response(response)

    def stripe_card_payment(self, data_dict):
        try:
            card_details = {
                "type": "card",
                "card": {
                    "number": data_dict['card_number'],
                    "exp_month": data_dict['expiry_month'],
                    "exp_year": data_dict['expiry_year'],
                    "cvc": data_dict['cvc']
                }
            }

            payment_intent = stripe.PaymentIntent.create(
                amount=10000,
                currency='inr',
                payment_method_data=card_details,
            )

            payment_confirm = stripe.PaymentIntent.confirm(
                payment_intent.id
            )

            if payment_confirm.status == 'succeeded':
                response = {
                    'message': "Card Payment Success",
                    'status': status.HTTP_200_OK,
                    "card_details": card_details,
                    "payment_intent": payment_confirm,
                }
            else:
                response = {
                    'message': "Card Payment Failed",
                    'status': status.HTTP_400_BAD_REQUEST,
                    "card_details": card_details,
                    "payment_intent": payment_confirm,
                }
        except stripe.error.CardError as e:
            response = {
                'error': e.error.message,
                'status': status.HTTP_400_BAD_REQUEST,
                "payment_intent": {"id": "Null"},
                "payment_confirm": {'status': "Failed"}
            }
        except stripe.error.APIError as e:
            response = {
                'error': "Stripe API Error: {}".format(e),
                'status': status.HTTP_400_BAD_REQUEST,
                "payment_intent": {"id": "Null"},
                "payment_confirm": {'status': "Failed"}
            }
        except Exception as e:
            response = {
                'error': "An unexpected error occurred: {}".format(e),
                'status': status.HTTP_400_BAD_REQUEST,
                "payment_intent": {"id": "Null"},
                "payment_confirm": {'status': "Failed"}
            }

        return response