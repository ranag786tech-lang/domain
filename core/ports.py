# core/ports.py
from abc import ABC, abstractmethod
from typing import Protocol
from domain.models import NotificationRequest, NotificationTemplate


class NotificationSender(Protocol):
    """Port: Interface for sending notifications via a channel."""
    @abstractmethod
    def send(self, request: NotificationRequest, content: str) -> bool:
        pass


class TemplateRenderer(Protocol):
    """Port: Interface for rendering templates with context."""
    @abstractmethod
    def render(self, template: NotificationTemplate, context: dict) -> str:
        pass


class NotificationRepository(Protocol):
    """Port: Interface for data persistence."""
    @abstractmethod
    def get_template(self, template_id: str) -> NotificationTemplate:
        pass

    @abstractmethod
    def save_audit(self, request: NotificationRequest, status: str):
        pass
