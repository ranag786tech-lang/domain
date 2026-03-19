# adapters/senders.py
import logging
from typing import Dict
from domain.models import NotificationRequest, NotificationChannel
from core.ports import NotificationSender

logger = logging.getLogger(__name__)


class EmailSender(NotificationSender):
    def __init__(self, smtp_config: Dict):
        self.smtp_config = smtp_config

    def send(self, request: NotificationRequest, content: str) -> bool:
        logger.info(f"[EMAIL] To {request.user.email}: {content[:50]}...")
        # Actual SMTP integration here
        return True


class SlackSender(NotificationSender):
    def __init__(self, bot_token: str):
        self.token = bot_token

    def send(self, request: NotificationRequest, content: str) -> bool:
        logger.info(f"[SLACK] To {request.user.slack_id}: {content[:50]}...")
        # Slack Webhook logic
        return True


class SmsSender(NotificationSender):
    def send(self, request: NotificationRequest, content: str) -> bool:
        logger.info(f"[SMS] To {request.user.phone}: {content[:30]}...")
        # Twilio/etc. integration
        return True


class PushSender(NotificationSender):
    def send(self, request: NotificationRequest, content: str) -> bool:
        logger.info(f"[PUSH] To {request.user.push_token}: {content[:30]}...")
        # Firebase/APNs logic
        return True
