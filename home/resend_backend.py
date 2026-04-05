# home/resend_backend.py

import resend
from django.core.mail.backends.base import BaseEmailBackend
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class ResendEmailBackend(BaseEmailBackend):
    def open(self):
        resend.api_key = settings.RESEND_API_KEY
        return True

    def close(self):
        pass

    def send_messages(self, email_messages):
        sent = 0
        resend.api_key = settings.RESEND_API_KEY

        for msg in email_messages:
            try:
                # Build params
                params = {
                    "from": msg.from_email,
                    "to": msg.to,
                    "subject": msg.subject,
                    "text": msg.body,
                }

                # Attach HTML alternative if present
                for content, mimetype in getattr(msg, 'alternatives', []):
                    if mimetype == 'text/html':
                        params["html"] = content
                        break

                resend.Emails.send(params)
                sent += 1
                logger.info(f"Resend: email sent to {msg.to}")
            except Exception as e:
                logger.error(f"Resend error: {e}")
                if not self.fail_silently:
                    raise

        return sent