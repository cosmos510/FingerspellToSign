# Parle avec tes mains

<div align="center">

**Real-time American Sign Language fingerspelling recognition powered by computer vision**

[![Live Demo](https://img.shields.io/badge/Live_Demo-parle--avec--tes--mains.fr-blue?style=for-the-badge)](https://parle-avec-tes-mains.fr)
[![Python](https://img.shields.io/badge/Python-3.8+-green?style=flat-square&logo=python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.0+-092E20?style=flat-square&logo=django)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

[Features](#key-features) • [Demo](#live-demo) • [Tech Stack](#tech-stack) • [Installation](#installation) • [Roadmap](#roadmap)

</div>

---

## About

**Parle avec tes mains** is a web application that helps people learn American Sign Language fingerspelling through real-time recognition. Using computer vision and machine learning, it provides instant feedback as you practice ASL letters with your webcam.

### The Challenge

- 70 million deaf people worldwide face daily communication barriers
- Traditional sign language learning requires expensive tutors and classes
- Learners lack instant feedback when practicing alone
- Quality learning resources remain inaccessible to many

### Our Solution

**Parle avec tes mains** makes ASL learning:
- **Instant** - Real-time recognition with sub-100ms latency
- **Accurate** - 95%+ recognition accuracy across various lighting conditions
- **Free** - No subscriptions or paywalls, fully open-source
- **Private** - Zero data collection, all processing happens locally
- **Accessible** - Works on any device with a camera

## Live Demo

<div align="center">

### [Try it now at parle-avec-tes-mains.fr](https://parle-avec-tes-mains.fr)

</div>

### How It Works

1. **Grant camera access** - One click to start
2. **Sign ASL letters** - Follow the visual guide
3. **Get instant feedback** - See predictions in real-time
4. **Build words** - Confirm letters to compose complete words

## Key Features

| Feature | Description |
|---------|-------------|
| **Real-time Recognition** | Instant ASL fingerspelling detection using MediaPipe hand tracking |
| **Interactive Alphabet** | Visual reference guide for all 26 ASL letters |
| **Word Builder** | Compose complete words letter by letter |
| **WCAG Compliant** | Full keyboard navigation and screen reader support |
| **Responsive Design** | Seamless experience on desktop, tablet, and mobile |
| **Privacy First** | No data storage, no tracking, no cookies |

## Tech Stack

### Backend
```python
Django 4.0+          # Web framework
MediaPipe            # Hand landmark detection
OpenCV               # Computer vision processing
Scikit-learn         # ML model training & inference
Random Forest        # Classifier (95%+ accuracy)
```

### Frontend
```javascript
Vanilla JavaScript   # Zero dependencies
WebRTC               # Browser camera access
CSS3                 # Modern responsive design
```

### ML Model
- **Input**: 21 hand landmarks (x, y, z coordinates)
- **Architecture**: Random Forest with 87 engineered features
- **Training**: 10,000+ images across 26 ASL letters
- **Accuracy**: >95% on test dataset
- **Inference**: <50ms per prediction

## Installation

### Prerequisites
```bash
Python 3.8+
pip
virtualenv (recommended)
```

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/parle-avec-tes-mains.git
cd parle-avec-tes-mains/asl_monolith

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your SECRET_KEY

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
```

### Access
```
http://localhost:8000
```

### Environment Variables

```env
SECRET_KEY=your-django-secret-key-here
DEBUG=False
DEFAULT_THEME=modern
```

## Screenshots

<div align="center">

### Homepage
![Homepage](static/asl.jpg)

### Live Recognition
![Prediction](static/detect.png)

</div>

## Use Cases

### For Learners
- Practice ASL alphabet at your own pace
- Get instant feedback without a tutor
- Track progress as you build words

### For Educators
- Free tool for classroom demonstrations
- Engage students with interactive learning
- Supplement traditional ASL curriculum

### For Developers
- Learn computer vision and ML implementation
- Contribute to accessibility technology
- Build upon open-source foundation

### For Healthcare
- Bridge communication gaps in medical settings
- Train staff on basic ASL communication
- Improve patient care for deaf community

## Roadmap

### 2024-2025

- [ ] French Sign Language (LSF) support
- [ ] Native iOS & Android applications
- [ ] Structured learning modules with progress tracking
- [ ] Multiplayer practice mode
- [ ] Full ASL vocabulary beyond fingerspelling
- [ ] Gamification features
- [ ] Public API access

## Impact

<div align="center">

| Metric | Value |
|--------|-------|
| **Potential Users** | 70M+ deaf people worldwide |
| **Recognition Speed** | <100ms latency |
| **Accuracy** | 95%+ across conditions |
| **Cost** | $0 - Completely free |
| **Data Collected** | 0 bytes - Privacy first |

</div>

## Contributing

Contributions are welcome! Here's how you can help:

1. **Report bugs** - Open an issue
2. **Suggest features** - Share your ideas
3. **Submit PRs** - Improve the code
4. **Improve docs** - Help others understand
5. **Translate** - Make it accessible globally

### Development Workflow
```bash
# Fork the repo, then:
git clone https://github.com/YOUR_USERNAME/parle-avec-tes-mains.git
cd parle-avec-tes-mains
git checkout -b feature/your-feature-name

# Make changes, test, commit
git commit -m "Add: your feature description"
git push origin feature/your-feature-name

# Open a Pull Request
```

## Security & Privacy

- No data collection or storage
- No user tracking or analytics
- No cookies or third-party scripts
- All processing happens locally
- Sensitive files protected via `.gitignore`

**Protected files:**
- `.env` - Secret keys
- `*.p` - ML models
- `db.sqlite3` - Database

## License

MIT License - free to use for learning, teaching, or building upon.

## Contact

<div align="center">

[![Email](https://img.shields.io/badge/Email-maximemartin510%40gmail.com-red?style=for-the-badge&logo=gmail)](mailto:maximemartin510@gmail.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Maxime_Martin-blue?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/maxime-martin-090731aa/)

</div>

### For Developers
Interested in the ML model or want to contribute? Reach out for technical documentation and collaboration opportunities.

### For Educators & Researchers
Looking to integrate this into educational programs or research? Let's discuss partnerships.

### For the Deaf Community
Your feedback shapes this project. Share your insights to make it more effective and inclusive.

---

<div align="center">

**Parle avec tes mains** - Breaking communication barriers through technology

[Live Demo](https://parle-avec-tes-mains.fr) • [Report Bug](https://github.com/yourusername/parle-avec-tes-mains/issues) • [Request Feature](https://github.com/yourusername/parle-avec-tes-mains/issues)

</div>
