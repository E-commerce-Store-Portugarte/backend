from django.apps import AppConfig


class EmailVerificationConfig(AppConfig):
    name = 'emailVerification'

    def ready(self):
        import emailVerification.signals

