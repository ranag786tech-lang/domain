# core/use_cases.py
import logging
from typing import Dict
from domain.models import NotificationRequest
from core.ports import (
    NotificationSender,
    TemplateRenderer,
    NotificationRepository,
)
from adapters.senders import (
    EmailSender,
    SlackSender,
    SmsSender,
    PushSender,
)

logger = logging.getLogger(__name__)


class SendNotificationUseCase:
    """Orchestrates the entire notification flow."""

    def __init__(
        self,
        repository: NotificationRepository,
        renderer: TemplateRenderer,
        sender_factory: Dict[str, NotificationSender],
        retry_attempts: int = 3,
    ):
        self.repository = repository
        self.renderer = renderer
        self.sender_factory = sender_factory
        self.retry_attempts = retry_attempts

    def execute(self, request: NotificationRequest) -> bool:
        # Fetch template
        template = self.repository.get_template(request.template_id)

        # Render content
        content = self.renderer.render(template, request.context)

        # Get sender for channel
        sender = self.sender_factory.get(request.channel.value)
        if not sender:
            logger.error(f"No sender for channel: {request.channel}")
            return False

        # Retry logic with exponential backoff
        for attempt in range(self.retry_attempts):
            try:
                success = sender.send(request, content)
                if success:
                    self.repository.save_audit(request, "SUCCESS")
                    logger.info(f"Notification sent successfully to {request.user.id}")
                    return True
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                # Exponential backoff
                time.sleep(2 ** attempt)

        self.repository.save_audit(request, "FAILED")
        return False
