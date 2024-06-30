from django.conf import settings
from django.conf import settings
from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from rest_framework import generics, status
from rest_framework.response import Response

from api.models.order import Order


@method_decorator(csrf_exempt, name='dispatch')
class WebhookVerifyPaystackPayment(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    
    PAYSTACK_SECRET_KEY = settings.PAYSTACK_SECRET_KEY
    paystack_base_url = 'https://api.paystack.co'

    def post(self, request, *args, **kwargs):
        DELIVERY_FEE = 1000
        try:
            with transaction.atomic():
                resp = json.loads(request.body.decode('utf-8'))
                ref = resp['data']['reference']
                verify_payment = self.verify_payment(ref)
                if not verify_payment['status']:
                    return Response({'detail': 'Payment not successful'}, status=status.HTTP_402_PAYMENT_REQUIRED)
                
                order = Order.objects.get(id=verify_payment['data']['metadata']['order_id'])
                if order.payment_ref == ref:
                    return Response({'detail': 'Already processed payment'}, status=status.HTTP_406_NOT_ACCEPTABLE)
                
                if not ((order.get_total_price_now() * 100) + DELIVERY_FEE <= verify_payment['data']['amount']):
                    order.payment_ref = ref
                    order.save()
                    return Response({'detail': 'Incomplete payment'}, status=status.HTTP_400_BAD_REQUEST)

                order.has_paid = True
                order.payment_ref = ref
                order.save()
                return Response({'detail': 'Success'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'detail': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def verify_payment(self, ref, *args, **kwargs):
        path = f"/transaction/verify/{ref}"
        headers = {
            "Authorization": f"Bearer {self.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json"
        }
        url = self.paystack_base_url + path
        res = requests.get(url, headers=headers)
        res_data = res.json()
        return res_data
