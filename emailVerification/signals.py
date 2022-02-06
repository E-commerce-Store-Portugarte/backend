from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from emailVerification.models import EmailToken, EmailVerified
from emailVerification.email_confirmation import template


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:

        email_token = EmailToken.objects.create(user=instance)
        EmailVerified.objects.create(user=instance)

        subject, from_email, to = 'Portugarte - Confirmação de compra', 'info@portugarte.pt', instance.email
        html_content = template.format(email_token.confirmation_url(), email_token.confirmation_url(), email_token.confirmation_url())
        msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
