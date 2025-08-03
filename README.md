# Telemedicine Backend API

A Django REST API backend for telemedicine applications with JWT authentication, role-based access control, appointment management, and real-time doctor status updates.

## Features

- JWT-based authentication with Doctor/Patient roles
- User registration and profile management
- Appointment booking and management system
- Real-time doctor status updates via WebSocket
- Comprehensive API documentation with Swagger
- Role-based permissions and security
- Docker containerization
- Unit tests and logging

## Tech Stack

- **Backend**: Django 4.2, Django REST Framework
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Database**: PostgreSQL/SQLite
- **Real-time**: Django Channels + Redis
- **Documentation**: drf-yasg (Swagger)
- **Containerization**: Docker, Docker Compose

## Quick Start

### Docker Setup (Recommended)

```bash
# Clone repository
git clone https://github.com/yourusername/telemedicine-backend.git
cd telemedicine-backend

# Start services
docker-compose up --build

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser (optional)
docker-compose exec web python manage.py createsuperuser
```

### Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start Redis for WebSocket
redis-server

# Run server
python manage.py runserver
```

## API Endpoints

- **Authentication**: `/api/auth/register/`, `/api/auth/login/`, `/api/auth/logout/`
- **User Management**: `/api/auth/profile/`, `/api/auth/doctors/`
- **Appointments**: `/api/appointments/`, `/api/appointments/create/`
- **WebSocket**: `ws://localhost:8000/ws/doctors-status/`
- **Documentation**: `/swagger/`, `/redoc/`

## Project Structure

```
telemedicine-backend/
├── telemedicine/          # Main Django project
├── users/                 # User management app
├── appointments/          # Appointment management app
├── requirements.txt       # Dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Multi-container setup
└── README.md            # This file
```

## Testing

```bash
# Run tests
python manage.py test

# With Docker
docker-compose exec web python manage.py test
```

## Environment Variables

Create `.env` file:

```env
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
REDIS_URL=redis://localhost:6379/0
```

## API Usage Examples

### User Registration
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "patient1",
    "email": "patient@example.com",
    "password": "securepass123",
    "password_confirm": "securepass123",
    "role": "patient"
  }'
```

### Create Appointment
```bash
curl -X POST http://localhost:8000/api/appointments/create/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "doctor": 2,
    "appointment_datetime": "2024-12-01T10:00:00Z",
    "symptoms": "Fever and headache"
  }'
```

