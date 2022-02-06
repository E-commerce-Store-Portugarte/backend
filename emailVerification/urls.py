from django.urls import path

from emailVerification.views import verify_email

urlpatterns = [
    path('verify/<str:verification_token>/', verify_email),
]