from django.shortcuts import render
from emailVerification.models import EmailToken, EmailVerified
from django.core.exceptions import ObjectDoesNotExist, ValidationError


def verify_email(request, verification_token):

    try:
        token = EmailToken.objects.get(token=verification_token)
    except (ValidationError, ObjectDoesNotExist):
        return render(request, 'emailVerification/index.html', {"message": "ERROR: Bad link"})

    email = EmailVerified.objects.get(user=token.user)
    email.is_verified = True
    email.save()
    token.delete()

    return render(request, 'emailVerification/index.html', {"message": "Email verified successfully"})
