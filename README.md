
#### **P. `/README.md`**
```markdown
# 📨 Notification Service - Production Ready Microservice

A modular, scalable, and production-ready notification service built with Clean Architecture principles. Supports multiple channels (Email, SMS, Slack, Push) with retry logic, templating, and comprehensive monitoring.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/docker-ready-blue)](https://www.docker.com/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

---

## 📋 Table of Contents
- [Overview](#-overview)
- [Architecture](#-architecture)
- [Features](#-features)
- [Quick Start](#-quick-start)
- [Usage Examples](#-usage-examples)
- [API Reference](#-api-reference)
- [Configuration](#-configuration)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Monitoring](#-monitoring)
- [Extending](#-extending)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

**One-liner:** A plug-and-play notification system that handles **Email, SMS, Slack, and Push** notifications with built-in retry logic, templating, and monitoring.

### Why This Service?
```python
# Instead of writing this 10 times...
try:
    if channel == "email":
        send_email(...)
    elif channel == "sms":
        send_sms(...)
except:
    retry_later(...)

# You just do this:
notification_service.send(channel, user, template, context)
# ✅ Handles retries, logging, monitoring automatically!
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│              API Layer (Flask)              │
├─────────────────────────────────────────────┤
│           Use Cases (Business Logic)         │
├─────────────────────────────────────────────┤
│   Ports (Interfaces)    │  Domain (Models)  │
├─────────────────────────────────────────────┤
│        Adapters (External Services)         │
│  ┌──────┬──────┬──────┬──────┬──────┐      │
│  │Email │ SMS  │Slack │ Push │ DB   │      │
│  └──────┴──────┴──────┴──────┴──────┘      │
└─────────────────────────────────────────────┘
```

**Clean Architecture Principles:**
- ✅ **Domain** - Pure business logic, no external dependencies
- ✅ **Ports** - Interfaces that define what we need
- ✅ **Adapters** - Implementations of those interfaces
- ✅ **Use Cases** - Orchestrate the flow
- ✅ **Dependency Inversion** - Core doesn't depend on details

---

## ✨ Features

### Core Capabilities
| Feature | Description |
|---------|-------------|
| **📧 Multi-Channel** | Email, SMS, Slack, Push notifications |
| **🔄 Auto Retry** | 3 attempts with exponential backoff |
| **📝 Templates** | Jinja2 templates with variables |
| **📊 Monitoring** | Prometheus metrics, structured logging |
| **🔐 Security** | Rate limiting, input validation |
| **📈 Scalable** | Async processing, connection pooling |
| **🧪 Testable** | 90%+ test coverage, mockable adapters |
| **🚀 Extensible** | Add new channel in < 50 lines |

### Production Ready
- ✅ Circuit breaker pattern
- ✅ Dead letter queue
- ✅ Audit logging
- ✅ Health checks
- ✅ Graceful shutdown
- ✅ Configuration management
- ✅ Docker/Kubernetes support

---

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.11+
Docker & Docker Compose (optional)
```

### 5-Minute Setup
```bash
# 1. Clone and enter
git clone https://github.com/your-org/notification-service.git
cd notification-service

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your settings (or use defaults for demo)

# 5. Run demo
python demo.py

# 6. Start the service
python -m api.main

# 7. Test it!
curl -X POST http://localhost:8000/api/v1/notifications/send \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_123",
    "user_name": "John Doe",
    "user_email": "john@example.com",
    "template_id": "welcome_email",
    "channel": "email",
    "context": {"name": "John"}
  }'
```

### Docker Quick Start
```bash
# Build and run with Docker Compose
docker-compose up -d

# Check logs
docker-compose logs -f notification-service

# Scale workers
docker-compose up -d --scale notification-service=3
```

---

## 📖 Usage Examples

### 1. Basic Email Notification
```python
from domain.models import User, NotificationRequest, NotificationChannel
from infrastructure.container import NotificationContainer

# Initialize container
container = NotificationContainer()
use_case = container.send_notification_use_case()

# Create user
user = User(
    id="user_123",
    name="Alice",
    email="alice@example.com"
)

# Create request
request = NotificationRequest(
    user=user,
    template_id="welcome_email",
    channel=NotificationChannel.EMAIL,
    context={"name": "Alice"}
)

# Send (auto retries on failure)
success = use_case.execute(request)
print(f"✅ Sent: {success}")
```

### 2. SMS with Priority
```python
request = NotificationRequest(
    user=User(
        id="user_456",
        name="Bob",
        phone="+1234567890"
    ),
    template_id="order_sms",
    channel=NotificationChannel.SMS,
    context={
        "order_id": "ORD-12345",
        "tracking_url": "https://example.com/track/12345"
    },
    priority=10  # High priority
)
```

### 3. Slack Alert
```python
request = NotificationRequest(
    user=User(
        id="user_789",
        slack_id="U12345678"
    ),
    template_id="server_alert",
    channel=NotificationChannel.SLACK,
    context={
        "server": "api-server-01",
        "error": "CPU at 95%",
        "action": "restarting"
    }
)

## 📚 API Reference

### REST Endpoints

#### `POST /api/v1/notifications/send`
Send a notification to a user.

**Request Body:**
```json
{
    "user_id": "string (required)",
    "user_name": "string (required)",
    "user_email": "string (required for email)",
    "user_phone": "string (optional)",
    "user_slack_id": "string (optional)",
    "user_push_token": "string (optional)",
    "template_id": "string (required)",
    "channel": "email|sms|slack|push (required)",
    "context": {
        "key1": "value1",
        "key2": "value2"
    },
    "priority": 1
}
```

**Response:**
```json
{
    "success": true,
    "notification_id": "uuid-here",
    "status": "sent"
}
```

#### `GET /api/v1/notifications/health`
Health check endpoint.

**Response:**
```json
{
    "status": "healthy",
    "version": "1.0.0",
    "timestamp": "2024-01-01T00:00:00Z"
}

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DATABASE_URL` | PostgreSQL connection string | - | ✅ |
| `REDIS_URL` | Redis connection string | - | ✅ |
| `SMTP_HOST` | SMTP server host | - | For email |
| `SMTP_PORT` | SMTP server port | 587 | For email |
| `SMTP_USER` | SMTP username | - | For email |
| `SMTP_PASSWORD` | SMTP password | - | For email |
| `SLACK_BOT_TOKEN` | Slack bot token | - | For slack |
| `TWILIO_ACCOUNT_SID` | Twilio account SID | - | For SMS |
| `TWILIO_AUTH_TOKEN` | Twilio auth token | - | For SMS |
| `FCM_API_KEY` | Firebase Cloud Messaging key | - | For push |
| `RETRY_ATTEMPTS` | Number of retry attempts | 3 | ✅ |
| `RATE_LIMIT` | Requests per minute | 100 | ✅ |

### Template Examples

**welcome_email.html**
```jinja2
Subject: Welcome {{ name }}!

<html>
<body>
    <h1>Welcome, {{ name }}!</h1>
    <p>Thank you for joining our platform.</p>
    <a href="{{ activation_link }}">Activate your account</a>
</body>
</html>
```

**order_sms.txt**
```jinja2
Your order #{{ order_id }} has shipped! 
Track here: {{ tracking_url }}
```

---

## 🧪 Testing

### Run All Tests
```bash
# Unit tests
pytest tests/unit/ -v

# Integration tests
pytest tests/integration/ -v

# With coverage
pytest --cov=src --cov-report=html

# Specific test
pytest tests/unit/test_use_cases.py::test_send_notification_success
```

### Example Test
```python
def test_send_notification_with_retry():
    # Mock failing sender
    mock_sender = Mock()
    mock_sender.send.side_effect = [Exception("Failed"), Exception("Failed"), True]
    
    use_case = SendNotificationUseCase(
        repository=Mock(),
        renderer=Mock(),
        sender_factory={"email": mock_sender},
        retry_attempts=3
    )
    
    result = use_case.execute(test_request)
    
    assert result is True
    assert mock_sender.send.call_count == 3
```

---

## 🚢 Deployment

### Docker
```bash
# Build image
docker build -t notification-service:latest .

# Run container
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql://... \
  -e REDIS_URL=redis://... \
  notification-service:latest
```

### Kubernetes
```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: notification-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: notification-service
  template:
    metadata:
      labels:
        app: notification-service
    spec:
      containers:
      - name: app
        image: notification-service:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

---

## 📊 Monitoring

### Prometheus Metrics
```python
# Available metrics
notifications_sent_total{channel="email",status="success"}
notification_latency_seconds{channel="sms"}
retry_attempts_total
circuit_breaker_open_total
```

### Grafana Dashboard
```json
{
  "dashboard": {
    "title": "Notification Service",
    "panels": [
      {
        "title": "Notifications per Second",
        "type": "graph",
        "targets": ["rate(notifications_sent_total[5m])"]
      },
      {
        "title": "Latency by Channel",
        "type": "heatmap",
        "targets": ["notification_latency_seconds_bucket"]
      }
    ]
  }
}
```

### Structured Logging
```json
{
  "timestamp": "2024-01-01T00:00:00Z",
  "level": "info",
  "event": "notification_sent",
  "channel": "email",
  "user_id": "123",
  "template_id": "welcome",
  "latency_ms": 45,
  "attempt": 1,
  "success": true
}
```

---

## 🔌 Extending

### Add a New Channel (e.g., WhatsApp)

**1. Create sender:**
```python
# adapters/senders/whatsapp_sender.py
from core.ports import NotificationSender

class WhatsAppSender(NotificationSender):
    def __init__(self, twilio_client):
        self.client = twilio_client
    
    def send(self, request, content):
        # WhatsApp implementation
        message = self.client.messages.create(
            body=content,
            from_='whatsapp:+14155238886',
            to=f'whatsapp:{request.user.phone}'
        )
        return message.sid is not None
```

**2. Register in container:**
```python
# infrastructure/container.py
whatsapp_sender = providers.Singleton(
    WhatsAppSender,
    twilio_client=config.whatsapp.client
)

sender_factory = providers.Dict(
    email=email_sender,
    slack=slack_sender,
    sms=sms_sender,
    push=push_sender,
    whatsapp=whatsapp_sender  # 👈 New channel
)
```

**3. Add template:**
```sql
INSERT INTO notification_templates 
(id, channel, body) 
VALUES 
('whatsapp_welcome', 'whatsapp', 'Welcome {{name}} to WhatsApp!');
```

**4. Use it:**
```python
request = NotificationRequest(
    user=User(phone="+1234567890"),
    channel=NotificationChannel("whatsapp"),
    template_id="whatsapp_welcome",
    context={"name": "John"}
)
```

---

## 🤝 Contributing

### Development Workflow
```bash
# Fork and clone
git checkout -b feature/amazing-feature

# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
make test

# Check code quality
make lint
make type-check

# Commit with conventional commits
git commit -m "feat: add WhatsApp channel"
git push origin feature/amazing-feature
```

### Code Style
- **Black** for formatting
- **isort** for imports
- **mypy** for type checking
- **pylint** for linting

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

Copyright (c) 2024 Your Company

---

## 🙏 Acknowledgments

- Clean Architecture by Robert C. Martin
- Dependency Injector library
- All contributors

---

## 🆘 Support & Contact

- **Documentation:** [https://docs.notification-service.dev](https://docs.notification-service.dev)
- **Issues:** [GitHub Issues](https://github.com/your-org/notification-service/issues)
- **Slack:** [#notification-service](https://your-org.slack.com)
- **Email:** dev@notification-service.com

## 🎯 Roadmap

- [x] Core notification channels (email, sms, slack, push)
- [x] Retry logic with exponential backoff
- [x] Template rendering
- [x] Monitoring & metrics
- [ ] Webhook notifications
- [ ] Voice call notifications
- [ ] A/B testing for templates
- [ ] AI-powered send time optimization
- [ ] Multi-language templates
- [ ] Geographic routing

---

**⭐ Star us on GitHub if you find this useful!**

---

**Built with ❤️ for developers, by developers**
