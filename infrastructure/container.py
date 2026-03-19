# infrastructure/container.py
from dependency_injector import containers, providers
from adapters.senders import EmailSender, SlackSender, SmsSender, PushSender
from adapters.renderers import Jinja2Renderer
from adapters.repositories import SQLNotificationRepository
from core.use_cases import SendNotificationUseCase


class NotificationContainer(containers.DeclarativeContainer):
    """IoC Container – wires all dependencies."""

    config = providers.Configuration()

    # Repository
    repository = providers.Singleton(
        SQLNotificationRepository,
        db_url=config.db.url,
    )

    # Renderer
    renderer = providers.Singleton(
        Jinja2Renderer,
        template_dir=config.templates.dir,
    )

    # Senders
    email_sender = providers.Singleton(
        EmailSender,
        smtp_config=config.email,
    )

    slack_sender = providers.Singleton(
        SlackSender,
        bot_token=config.slack.token,
    )

    sms_sender = providers.Singleton(
        SmsSender,
        twilio_account=config.sms.account,
    )

    push_sender = providers.Singleton(
        PushSender,
        fcm_key=config.push.fcm_key,
    )

    # Sender factory mapping
    sender_factory = providers.Dict(
        email=email_sender,
        slack=slack_sender,
        sms=sms_sender,
        push=push_sender,
    )

    # Use case
    send_notification_use_case = providers.Factory(
        SendNotificationUseCase,
        repository=repository,
        renderer=renderer,
        sender_factory=sender_factory,
        retry_attempts=config.retry.attempts,
    )
