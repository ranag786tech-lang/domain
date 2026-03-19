# api/controllers.py
from flask import Blueprint, request, jsonify
from dependency_injector.wiring import inject, Provide
from domain.models import User, NotificationRequest, NotificationChannel
from core.use_cases import SendNotificationUseCase
from infrastructure.container import NotificationContainer

notifications_bp = Blueprint("notifications", __name__)


@notifications_bp.route("/send", methods=["POST"])
@inject
def send_notification(
    use_case: SendNotificationUseCase = Provide[NotificationContainer.send_notification_use_case],
):
    data = request.json

    user = User(
        id=data["user_id"],
        name=data["user_name"],
        email=data["user_email"],
        phone=data.get("user_phone"),
    )

    notification_request = NotificationRequest(
        user=user,
        template_id=data["template_id"],
        channel=NotificationChannel(data["channel"]),
        context=data.get("context", {}),
    )

    success = use_case.execute(notification_request)

    return jsonify({"success": success}), 200 if success else 500
