# ASL Recognition - Monolithic Version

A simplified, single-application version of the ASL Alphabet Recognition system, designed for easy deployment and demonstration.

## 🚀 Quick Start

1. **Clone and navigate to the project:**
   ```bash
   cd asl_monolith
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run setup:**
   ```bash
   python setup.py
   ```

4. **Start the server:**
   ```bash
   python manage.py runserver
   ```

5. **Visit the app:**
   Open http://localhost:8000 in your browser

## 📋 Features

- **Real-time ASL recognition** via webcam
- **Clean, responsive UI**
- **No registration required** - just start using it!
- **SQLite database** (no external database required)

## 🛠️ Technology Stack

- **Backend:** Django 4.2
- **Database:** SQLite (included)
- **ML:** Scikit-learn, MediaPipe, OpenCV
- **Frontend:** HTML, CSS, JavaScript

## 📁 Project Structure

```
asl_monolith/
├── asl_app/          # Django project settings
├── core/             # Main application
├── templates/        # HTML templates
├── static/           # CSS, JS, images
├── model1.p          # Pre-trained ML model
├── requirements.txt  # Dependencies
└── setup.py         # Setup script
```

## 🔧 Development

- **Admin panel:** http://localhost:8000/admin
- **Create superuser:** `python manage.py createsuperuser`
- **Run tests:** `python manage.py test`

## 📝 Notes

- This is a simplified version optimized for demonstration
- Uses SQLite for easy setup (no PostgreSQL required)
- No user registration or authentication required
- Direct access to ASL recognition functionality

## 🌐 Deployment

For production deployment:
1. Set `DEBUG = False` in settings.py
2. Configure proper SECRET_KEY
3. Set up proper email backend
4. Use a production database (PostgreSQL/MySQL)
5. Configure static files serving

Perfect for showcasing to recruiters and quick demos!