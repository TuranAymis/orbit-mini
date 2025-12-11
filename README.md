# Mini Orbit - Refactored

### CS50 Final Project by Turan Aymış

---

## 🚀 What's New

This version has been refactored from a monolithic Flask application into a **professional, scalable architecture** using:

- ✅ **Application Factory Pattern**
- ✅ **Blueprint-based Modular Structure**
- ✅ **Environment-based Configuration**
- ✅ **Improved Code Organization**

---

## 📁 New Project Structure

```
orbit-mini/
├── app/
│   ├── __init__.py              # Application Factory
│   ├── auth/                    # Authentication Blueprint
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── events/                  # Events Blueprint
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── main/                    # Main Blueprint
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── templates/               # Jinja2 templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── profile.html
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   └── events/
│   │       └── add.html
│   └── static/
│       └── css/
│           └── main.css
├── config.py                    # Configuration classes
├── run.py                       # Application entry point
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore rules
├── requirements.txt             # Python dependencies
├── orbit.db                     # SQLite database
└── README.md                    # This file
```

---

## 🔧 Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file (copy from `.env.example`):

```bash
cp .env.example .env
```

Edit `.env` and set your configuration:

```env
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///orbit.db
```

### 3. Run the Application

```bash
# Using Flask CLI
flask run

# Or using Python directly
python run.py
```

The application will be available at `http://localhost:5000`

---

## 🎯 Features

All original features are preserved:

- ✅ User registration and authentication
- ✅ Create events with capacity limits
- ✅ Join/leave events
- ✅ Profile page (created + joined events)
- ✅ Google Maps integration
- ✅ Event capacity management
- ✅ Responsive Bootstrap 5 UI

---

## 🏗️ Architecture Improvements

### Application Factory Pattern

The app is now created using a factory function, allowing:
- Multiple app instances with different configurations
- Easier testing
- Better separation of concerns

### Blueprint Structure

Routes are organized into logical modules:
- **auth**: `/auth/login`, `/auth/register`, `/auth/logout`
- **events**: `/events/add`, `/events/join/<id>`, `/events/leave/<id>`, `/events/delete/<id>`
- **main**: `/` (homepage), `/profile`

### Configuration Management

Environment-specific settings in `config.py`:
- `DevelopmentConfig` - Debug mode, verbose logging
- `ProductionConfig` - Optimized for deployment
- `TestingConfig` - For unit tests

---

## 📝 API Routes

| Route | Blueprint | Method | Auth | Description |
|-------|-----------|--------|------|-------------|
| `/` | main | GET | No | Homepage - list all events |
| `/profile` | main | GET | Yes | User profile |
| `/auth/register` | auth | GET, POST | No | User registration |
| `/auth/login` | auth | GET, POST | No | User login |
| `/auth/logout` | auth | GET | No | User logout |
| `/events/add` | events | GET, POST | Yes | Create event |
| `/events/join/<id>` | events | GET | Yes | Join event |
| `/events/leave/<id>` | events | GET | Yes | Leave event |
| `/events/delete/<id>` | events | POST | Yes | Delete event |

---

## 🔐 Security Features

- ✅ Password hashing (Werkzeug)
- ✅ Server-side session management
- ✅ SQL injection protection (parameterized queries)
- ✅ Authorization checks
- ✅ Environment-based secrets
- ✅ Cache control headers

---

## 🚀 Deployment

### Production Checklist

1. Set `FLASK_ENV=production` in `.env`
2. Generate a strong `SECRET_KEY`
3. Use a production WSGI server (Gunicorn included)
4. Consider migrating to PostgreSQL for better concurrency
5. Enable HTTPS

### Running with Gunicorn

```bash
gunicorn -w 4 -b 0.0.0.0:8000 "app:create_app()"
```

---

## 📚 Technologies Used

- **Python 3**
- **Flask 3.0.3** - Web framework
- **Flask-Session 0.5.0** - Session management
- **SQLite** - Database
- **CS50 Library** - SQL interface
- **Werkzeug 3.0.2** - Security utilities
- **Bootstrap 5** - Frontend framework
- **Jinja2** - Template engine
- **Gunicorn** - WSGI server
- **python-dotenv** - Environment variables

---

## 🎓 Learning Outcomes

This refactored version demonstrates:
- **Application Factory Pattern** for scalable Flask apps
- **Blueprint architecture** for modular code organization
- **Environment-based configuration** for different deployment scenarios
- **Professional project structure** following Flask best practices
- **Separation of concerns** between routes, templates, and configuration

---

## 📹 Video Demo

https://youtu.be/XTHVzvlYF_c

---

## 👨‍💻 Author

**Turan Aymış**  
CS50 Final Project - Refactored Edition

---

## 📄 License

This project is open source and available for educational purposes.
