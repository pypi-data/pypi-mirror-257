"""
Конфигурация приложения backend
"""

from django.apps import AppConfig
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.core.validators import URLValidator


class MailingBackendConfig(AppConfig):
    """
    Приложение отвечающие за backend рассылки
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "mailing_backend"

    def ready(self) -> None:
        if not hasattr(settings, "EMAIL_ENDPOINT_URL"):
            raise ImproperlyConfigured("Set EMAIL_ENDPOINT_URL in your settings file.")

        try:
            URLValidator()(settings.EMAIL_ENDPOINT_URL)  # type: ignore[misc]
        except ValidationError as exc:
            raise ImproperlyConfigured(
                "EMAIL_ENDPOINT_URL must be a valid URL."
            ) from exc
