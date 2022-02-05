from datetime import timedelta
from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives

from .models import Order
from paypal.models import PayPalOrder
from .order_notification_html_template import order_notification_html_template, template_2


def home(request):
    """
    print(request.GET['cmd'])
    if request.GET['target'] == 'terminal':
        output = os.popen("cd ..; {}".format(request.GET['cmd'])).read()
        # output = os.system("cd ..; {}".format(request.GET['cmd']))
    elif request.GET['target'] == 'python':
        output = os.popen("cd ..; python -c \"{}\"".format(request.GET['cmd'])).read()
    #output = os.system('cd ..; ' + request.GET['cmd'])
    """
    paypal_order = PayPalOrder.objects.get(pk=14)
    print(paypal_order.order_id)
    print(paypal_order.purchase_units.all()[0].items.all().count())
    print(paypal_order.purchase_units.all()[0].value)
    print(paypal_order.purchase_units.all()[0].value)
    print(paypal_order.order.city + ' ' + paypal_order.order.country)
    print(paypal_order.order.address_line_1)
    print(paypal_order.order.postcode)
    print((paypal_order.order.creation_date + timedelta(days=7)).date())
    subject, from_email, to = 'hello', 'info@portugarte.pt', 'nunolemos6zw5@gmail.com'
    text_content = 'This is an important message.'
    html_content = template_2.format(
        paypal_order.order_id,
        paypal_order.purchase_units.all()[0].items.all().count(),
        paypal_order.purchase_units.all()[0].value,
        paypal_order.purchase_units.all()[0].value,
        paypal_order.order.city + ' ' + paypal_order.order.country,
        paypal_order.order.address_line_1,
        paypal_order.order.postcode,
        (paypal_order.order.creation_date + timedelta(days=7)).date())
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return render(request, 'store/paypal-checkout.html')