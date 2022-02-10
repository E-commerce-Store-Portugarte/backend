import uuid

from django.db import models
from django.contrib.auth import get_user_model

from EcomApp import settings

User = get_user_model()


def generate_verification_token():
    return uuid.uuid4()


class EmailVerified(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)


class EmailToken(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=generate_verification_token, unique=True)

    def confirmation_url(self):
        return settings.CURRENT_HOST + '/email/verify/{}/'.format(self.token)
