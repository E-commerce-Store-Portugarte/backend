import json

from django.core.mail import send_mail
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
from paypal.models import PayPalOrder, PayPalPayer, PayPalShippingAddress
from store.models import Order, PrePaymentOrder, OrderItem
import requests


@require_http_methods(['POST'])
@csrf_exempt
def paypal_webhooks(request):

    webhook_event = request.body.decode('utf-8')
    webhook_event = json.loads(webhook_event)
    data = {
        "transmission_id": request.headers['Paypal-Transmission-Id'],
        "transmission_time": request.headers['Paypal-Transmission-Time'],
        "cert_url": request.headers['Paypal-Cert-Url'],
        "auth_algo": request.headers['Paypal-Auth-Algo'],
        "transmission_sig": request.headers['Paypal-Transmission-Sig'],
        "webhook_id": settings.PAYPAL_WEBHOOK_ID,
        "webhook_event": webhook_event
    }
    print(webhook_event, "WEBHOOK")
    response = requests.post(url='https://api-m.sandbox.paypal.com/v1/notifications/verify-webhook-signature',
        auth=(settings.PAYPAL_CLIENT_ID, settings.PAYPAL_CLIENT_SECRET),
        headers={ "Content-Type": "application/json"},
        data=json.dumps(data))
    if response.json()['verification_status'] == 'SUCCESS':
        if webhook_event['event_type'] == 'CHECKOUT.ORDER.APPROVED':
            paypal_order = PayPalOrder.objects.get(order_id=webhook_event['resource']['id'])
            pre_payment_order = PrePaymentOrder.objects.get(paypal_order=paypal_order)

            send_mail('Olá {}'.format(pre_payment_order.full_name),
                      'Compra feita no valor de {}'.format(paypal_order.purchase_units[0].value),
                      'info@portugarte.pt',
                      [pre_payment_order.email],
                      fail_silently=False
                      )
            api_data = paypal_order.capture()
            if api_data['status'] == 'COMPLETED':
                payer_object, created = PayPalPayer.objects.get_or_create(
                    user=pre_payment_order.buyer,
                    given_name=webhook_event['resource']['payer']['name']['given_name'],
                    surname=webhook_event['resource']['payer']['name']['surname'],
                    email_address=webhook_event['resource']['payer']['email_address'],
                    paypal_id=webhook_event['resource']['payer']['payer_id'],
                    country_code=webhook_event['resource']['payer']['address']['country_code']
                )
                paypal_order.order_status = 'COMPLETED'
                paypal_order.buyer = payer_object
                paypal_order.save()
                order = Order.objects.create(
                    paypal_order=paypal_order,
                    buyer=pre_payment_order.buyer,
                    full_name=pre_payment_order.full_name,
                    email=pre_payment_order.email,
                    phone_number=pre_payment_order.phone_number,
                    city=pre_payment_order.city,
                    address_line_1=pre_payment_order.address_line_1,
                    address_line_2=pre_payment_order.address_line_2,
                    postcode=pre_payment_order.postcode,
                    delivery_instructions=pre_payment_order.delivery_instructions,
                    country=pre_payment_order.country
                )

                key_list = ['address_line_1', 'address_line_2', 'admin_area_1', 'admin_area_2', 'postal_code', 'country_code']
                for key in key_list:
                    if key not in webhook_event['resource']['purchase_units'][0]['shipping']['address']:
                        webhook_event['resource']['purchase_units'][0]['shipping']['address'][key] = ''

                paypal_shipping_address = PayPalShippingAddress.objects.create(
                    address_line_1=webhook_event['resource']['purchase_units'][0]['shipping']['address']['address_line_1'],
                    address_line_2=webhook_event['resource']['purchase_units'][0]['shipping']['address']['address_line_2'],
                    admin_area_1=webhook_event['resource']['purchase_units'][0]['shipping']['address']['admin_area_1'],
                    admin_area_2=webhook_event['resource']['purchase_units'][0]['shipping']['address']['admin_area_2'],
                    postal_code=webhook_event['resource']['purchase_units'][0]['shipping']['address']['postal_code'],
                    country_code=webhook_event['resource']['purchase_units'][0]['shipping']['address']['country_code'],
                )

                for purchase_unit in paypal_order.purchase_units.all():
                    purchase_unit.shipping = paypal_shipping_address
                    purchase_unit.save()
                    for item in purchase_unit.items.all():
                        OrderItem.objects.create(
                            buyer=pre_payment_order.buyer,
                            order=order,
                            product=item.product,
                            amount=item.quantity
                        )

                return HttpResponse(status=200)
            return HttpResponse(status=200)
        return HttpResponse(status=200)
