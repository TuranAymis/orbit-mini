# Orbit Mini - Deployment Guide

This guide covers deploying the Orbit Mini event management application to production platforms like Render, Railway, or Heroku.

## Prerequisites

- Git repository initialized
- Python 3.8+ installed locally
- Account on deployment platform (Render/Railway/Heroku)

## Project Structure

```
orbit-mini/
├── app/                    # Application package
├── .env                    # Local environment variables (not in git)
├── .env.example            # Environment template for development
├── .env.production.example # Environment template for production
├── .gitignore              # Git ignore rules
├── config.py               # Configuration classes
├── init_db.py              # Database migration script
├── Procfile                # Production server configuration
├── requirements.txt        # Python dependencies
└── run.py                  # Application entry point
```

## Environment Configuration

### Development (.env)
```bash
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=dev-secret-key-change-in-production
DATABASE_URL=sqlite:///orbit.db
```

### Production
Copy `.env.production.example` and configure:

```bash
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=<generate-strong-random-key>
DATABASE_URL=sqlite:///orbit.db
```

> [!IMPORTANT]
> **Generate a secure SECRET_KEY** for production:
> ```python
> python -c "import secrets; print(secrets.token_hex(32))"
> ```

## Database Setup

The application uses SQLite by default. The database will be created automatically on first run.

### Initial Setup
1. The database file (`orbit.db`) will be created when the app first starts
2. Run migrations if needed: `python init_db.py`

### Production Considerations
- SQLite works well for small to medium applications
- For high-traffic apps, consider PostgreSQL (update `DATABASE_URL`)
- Ensure the database file has proper write permissions

## Deployment Platforms

### Render

1. **Create New Web Service**
   - Connect your GitHub repository
   - Select the repository

2. **Configure Build Settings**
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn "app:create_app()"`

3. **Environment Variables**
   Add in Render dashboard:
   ```
   FLASK_ENV=production
   FLASK_DEBUG=False
   SECRET_KEY=<your-secret-key>
   DATABASE_URL=sqlite:///orbit.db
   ```

4. **Deploy**
   - Click "Create Web Service"
   - Render will automatically deploy on git push

### Railway

1. **Create New Project**
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository

2. **Configure**
   Railway auto-detects the `Procfile`

3. **Environment Variables**
   Add in Railway dashboard:
   ```
   FLASK_ENV=production
   FLASK_DEBUG=False
   SECRET_KEY=<your-secret-key>
   DATABASE_URL=sqlite:///orbit.db
   ```

4. **Deploy**
   - Railway deploys automatically
   - Get your app URL from the dashboard

### Heroku

1. **Install Heroku CLI**
   ```bash
   # Login to Heroku
   heroku login
   ```

2. **Create App**
   ```bash
   heroku create orbit-mini-app
   ```

3. **Set Environment Variables**
   ```bash
   heroku config:set FLASK_ENV=production
   heroku config:set FLASK_DEBUG=False
   heroku config:set SECRET_KEY=<your-secret-key>
   ```

4. **Deploy**
   ```bash
   git push heroku main
   ```

5. **Open App**
   ```bash
   heroku open
   ```

## Local Testing (Production Mode)

Test production configuration locally:

```bash
# Set environment variables
export FLASK_ENV=production
export FLASK_DEBUG=False
export SECRET_KEY=test-secret-key

# Run with gunicorn
gunicorn "app:create_app()"
```

Access at: `http://localhost:8000`

## Post-Deployment Checklist

- [ ] Verify app is accessible via production URL
- [ ] Test user registration and login
- [ ] Test event creation and management
- [ ] Verify database persistence across restarts
- [ ] Check that debug mode is OFF (no stack traces visible)
- [ ] Verify SECRET_KEY is set and secure
- [ ] Test all major features work in production

## Troubleshooting

### App won't start
- Check logs: `heroku logs --tail` (Heroku) or view in dashboard (Render/Railway)
- Verify all environment variables are set
- Ensure `requirements.txt` is up to date

### Database errors
- Verify database file permissions
- Check `DATABASE_URL` is correct
- Run migration script: `python init_db.py`

### Session issues
- Verify `SECRET_KEY` is set
- Check `flask_session/` directory exists and is writable
- For filesystem sessions, ensure persistent storage

## Updating the Application

1. **Make changes locally**
2. **Test locally**
   ```bash
   python run.py
   ```
3. **Commit changes**
   ```bash
   git add .
   git commit -m "Description of changes"
   ```
4. **Push to GitHub**
   ```bash
   git push origin main
   ```
5. **Auto-deploy** (Render/Railway) or **Manual deploy** (Heroku):
   ```bash
   git push heroku main
   ```

## Security Best Practices

> [!CAUTION]
> - **Never commit `.env` file** (already in `.gitignore`)
> - **Use strong SECRET_KEY** in production
> - **Set FLASK_DEBUG=False** in production
> - **Use HTTPS** (enabled by default on Render/Railway/Heroku)
> - **Regularly update dependencies** for security patches

## Performance Optimization

- **Gunicorn workers**: Adjust in `Procfile` if needed
  ```
  web: gunicorn "app:create_app()" --workers 4
  ```
- **Database**: Consider PostgreSQL for production at scale
- **Static files**: Consider CDN for static assets
- **Caching**: Implement Redis for session storage if needed

## Support

For issues or questions:
- Check application logs
- Review this deployment guide
- Consult platform-specific documentation:
  - [Render Docs](https://render.com/docs)
  - [Railway Docs](https://docs.railway.app)
  - [Heroku Docs](https://devcenter.heroku.com)
