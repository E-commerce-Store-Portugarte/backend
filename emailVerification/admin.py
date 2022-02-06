from django.contrib import admin

from emailVerification.models import EmailToken, EmailVerified

admin.site.register(EmailToken)
admin.site.register(EmailVerified)
