# Fingerspell to Sign

Fingerspell to Sign is a web-based application designed to bridge the gap between fingerspelling and sign language recognition. This project leverages modern web technologies and a custom-trained machine learning model to provide an intuitive and interactive platform for users to explore and learn about sign language.

## Features

- **Sign Language Recognition**: Upload or interact with images to detect and recognize sign language gestures.
- **Interactive UI**: A user-friendly interface with dynamic elements for seamless navigation.
- **Static and Dynamic Content**: Includes static assets like images, CSS, and JavaScript for a visually appealing experience.
- **Django Backend**: Powered by Django, ensuring robust and scalable backend support.
- **Trained Model**: A custom-trained model (`model1.p`) for gesture recognition.

## Project Structure

The project is organized as follows:

```
asl_monolith/
├── db.sqlite3          # SQLite database
├── Dockerfile          # Docker configuration for containerization
├── manage.py           # Django management script
├── model1.p            # Pre-trained model for gesture recognition
├── requirements.txt    # Python dependencies
├── asl_app/            # Main Django app
│   ├── settings.py     # Django settings
│   ├── urls.py         # URL routing
│   ├── wsgi.py         # WSGI configuration
├── core/               # Core application logic
│   ├── models.py       # Database models
│   ├── views.py        # Application views
│   ├── urls.py         # Core URL routing
├── static/             # Static assets (images, CSS, JS)
├── staticfiles/        # Collected static files for deployment
├── templates/          # HTML templates
```

## Installation

To get started with the project, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/cosmos510/FingerspellToSign.git
   cd FingerspellToSign
   ```

2. Set up a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run database migrations:
   ```bash
   python manage.py migrate
   ```

5. Start the development server:
   ```bash
   python manage.py runserver
   ```

6. Access the application at `http://127.0.0.1:8000/`.

## Usage

- Navigate to the homepage to explore the features.
- Use the interactive UI to upload images or interact with the sign language recognition tool.
- Explore the `About` and `Predict` pages for more insights.

## Deployment

The project includes a `Dockerfile` for containerized deployment. To deploy using Docker:

1. Build the Docker image:
   ```bash
   docker build -t fingerspell-to-sign .
   ```

2. Run the Docker container:
   ```bash
   docker run -p 8000:8000 fingerspell-to-sign
   ```

3. Access the application at `http://127.0.0.1:8000/`.

## Screenshots

### Homepage
![Homepage](static/asl.jpg)

### Prediction Page
![Prediction Page](static/detect.png)

## Technologies Used

- **Backend**: Django
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite
- **Machine Learning**: Custom-trained model for gesture recognition
- **Containerization**: Docker

## Future Enhancements

- Add real-time video gesture recognition.
- Expand the dataset for improved accuracy.
- Integrate user authentication and profiles.

## Contributing

Contributions are welcome! Feel free to fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

For any inquiries or feedback, please contact:

- **Name**: Maxime Martin
- **Email**: maxime.martin@example.com
- **GitHub**: [cosmos510](https://github.com/cosmos510)

---

Thank you for exploring Fingerspell to Sign! We hope this project inspires you to learn more about sign language and its applications.
