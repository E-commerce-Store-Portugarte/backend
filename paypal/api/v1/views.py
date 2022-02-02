import json

from rest_framework.response import Response
from django.conf import settings
from store.models import BasketItem, PrePaymentOrder, Product
from rest_framework.decorators import api_view
from paypal.models import PayPalOrder, PayPalPurchaseUnit, PayPalMerchant, PayPalItem
import requests


NOT_AUTHENTICATED_ERROR = Response(data={"error": "You are not authenticated"}, status=401)


def build_request_body(user_basket):
    body = {
        # States that the payment should be received immediately
        "intent": "CAPTURE",
        "application_context": {
            # The URL where the customer is redirected after the customer approves the payment.
            "return_url": settings.CURRENT_HOST + "/success",
            # The URL where the customer is redirected after the customer cancels the payment.
            "cancel_url": settings.CURRENT_HOST + "basket",
            # The label that overrides the business name in the PayPal account on the PayPal site.
            "brand_name": "Portugarte"
        },

        # An array of purchase units. Each purchase unit establishes a contract
        # between a payer and the payee. Each purchase unit represents
        # either a full or partial order that the payer intends to purchase from the payee.
        # in this case its length will always be 1 since there is only 1 seller
        "purchase_units": [
            {
                # An object containing the total value of the transaction and the payment's currency code
                "amount": {
                    "currency_code": "EUR",
                    # Contains the same information as above
                    # "breakdown" is required due to the existence of "items" array
                    "breakdown": {
                        "item_total": {
                            "currency_code": "EUR"
                        }
                    },
                },
                # An array of items (object). Each object containing:
                # name: string
                # quantity: string
                # unit_amount: { value: string, currency_code: string }
                # the sum of all purchase_units[].items[].quantity * purchase_units[].items[].unit_amount.value
                # must be equal to purchase_units[].amount.value
                "items": []
            }
        ]
    }
    total_price = 0
    for basket_item in user_basket:
        if basket_item.amount > 0:
            item = {
                'name': basket_item.product.name,
                'description': str(basket_item.product.reference),
                'quantity': basket_item.amount,
                'unit_amount': {
                    'value': float(basket_item.product.price),
                    'currency_code': 'EUR'
                }
            }
            body['purchase_units'][0]['items'].append(item)
            total_price += basket_item.price()
        else:
            basket_item.delete()
    body['purchase_units'][0]['amount']['value'] = total_price
    body['purchase_units'][0]['amount']['breakdown']['item_total']['value'] = total_price
    return body


@api_view(["POST"])
def create_paypal_order(request):
    if request.user.is_authenticated:
        user_basket = BasketItem.objects.filter(user=request.user)
        if user_basket.count() > 0:
            response = requests.post(
                url='https://api-m.sandbox.paypal.com/v2/checkout/orders',
                auth=(settings.PAYPAL_CLIENT_ID, settings.PAYPAL_CLIENT_SECRET),
                json=build_request_body(user_basket)
            )
            response_json = response.json()
            print(response_json)
            if response_json['status'] == 'CREATED':
                order_details = requests.get(
                    url='https://api.sandbox.paypal.com/v2/checkout/orders/' + response_json['id'],
                    auth=(settings.PAYPAL_CLIENT_ID, settings.PAYPAL_CLIENT_SECRET),
                )
                order_data = order_details.json()
                paypal_order = PayPalOrder.objects.create(order_id=response_json['id'], order_status='CREATED')
                for purchase_unit in order_data['purchase_units']:
                    merchant, created = PayPalMerchant.objects.get_or_create(
                        paypal_id=purchase_unit['payee']['merchant_id'],
                        email_address=purchase_unit['payee']['email_address'],
                        brand_name=purchase_unit['payee']['display_data']['brand_name']
                    )
                    purchase_unit_object = PayPalPurchaseUnit.objects.create(
                        reference_id=purchase_unit['reference_id'],
                        currency_code=purchase_unit['amount']['currency_code'],
                        value=purchase_unit['amount']['value'],
                        order=paypal_order,
                        merchant=merchant
                    )
                    for item in purchase_unit['items']:
                        print(item, 'CREATED')
                        PayPalItem.objects.create(
                            purchase_unit=purchase_unit_object,
                            quantity=item['quantity'],
                            product=Product.objects.get(reference=item['description'])
                        )
                pre_payment_order = PrePaymentOrder.objects.create(
                    paypal_order=paypal_order, buyer=request.user, full_name=request.data['name'],
                    phone_number=request.data['phone'], email=request.data['email'], city=request.data['city'],
                    address_line_1=request.data['address'], postcode=request.data['postcode'], country="Portugal"
                )
                return Response(data={'redirect_url': pre_payment_order.approve()}, status=200)
        return Response(data={'error': 'Your basket is empty'}, status=400)
    return NOT_AUTHENTICATED_ERROR
