# domain/models.py
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, Any, Optional


class NotificationChannel(Enum):
    EMAIL = "email"
    SMS = "sms"
    SLACK = "slack"
    PUSH = "push"


@dataclass(frozen=True)
class User:
    id: str
    name: str
    email: str
    phone: Optional[str] = None
    slack_id: Optional[str] = None
    push_token: Optional[str] = None


@dataclass
class NotificationTemplate:
    id: str
    channel: NotificationChannel
    subject: Optional[str]
    body: str
    variables: Dict[str, Any]


@dataclass
class NotificationRequest:
    user: User
    template_id: str
    channel: NotificationChannel
    context: Dict[str, Any]
    priority: int = 1
