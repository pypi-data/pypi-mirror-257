"""
Backend для отправки рассылки в MC mailing
"""

import json
from typing import Sequence, Any
import logging
import requests
from django.core.mail.backends.base import BaseEmailBackend
from django.conf import settings
from django.core.mail.message import EmailMessage

logger = logging.getLogger(__name__)


class EndpointEmailBackend(BaseEmailBackend):
    """
    Класс для отправки электронных писем через JSON на указанный endpoint.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.endpoint_url = settings.EMAIL_ENDPOINT_URL  # type: ignore[misc]

    def send_messages(self, email_messages: Sequence[EmailMessage]) -> int:
        """
        Отправляет список электронных сообщений на указанный endpoint в формате JSON.
        """
        successfully_sent_count = 0

        if not email_messages:
            return 0

        for message in email_messages:
            # Собираем данные для отправки
            payload = {
                "subject": message.subject,
                "body": message.body,
                "email_list": message.to,
                "from_message": message.from_email,
            }
            headers = {"Content-Type": "application/json"}

            try:
                # Отправляем запрос на указанный в settings endpoint
                response = requests.post(
                    self.endpoint_url,
                    data=json.dumps(payload),
                    headers=headers,
                    timeout=30,
                )

                response.raise_for_status()

                if response.status_code == 201:
                    response_data = response.json()
                    successfully_sent_count += len(response_data["emails_sent"])

            except requests.exceptions.RequestException as exc:
                if self.fail_silently:
                    logger.error(exc)
                else:
                    raise exc
            except json.JSONDecodeError as exc:
                if self.fail_silently:
                    logger.error(exc)
                else:
                    raise exc
            except KeyError as exc:
                error_message = '"emails_sent" is not in the response.'
                if self.fail_silently:
                    logger.error(error_message)
                else:
                    raise KeyError(error_message) from exc

        return successfully_sent_count
