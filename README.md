# Signéo - ASL Fingerspelling Recognition

**Signéo** is a real-time American Sign Language (ASL) fingerspelling recognition web application that bridges the communication gap between deaf and hearing communities. Using advanced computer vision and machine learning, it provides instant recognition of ASL fingerspelling gestures through your webcam.

🌐 **Live Demo**: [Try Signéo](https://fingerspelltosign.up.railway.app)

## 🎯 Mission

Our mission is to democratize sign language learning by making fingerspelling accessible to everyone, everywhere, at any time. This project serves as the foundation for a more ambitious vision: translating complete sign language, not just fingerspelling.

## ✨ Key Features

- **Real-time Recognition**: Instant ASL fingerspelling detection through webcam
- **Interactive Learning**: Visual alphabet reference and step-by-step instructions
- **Word Building**: Compose words letter by letter with confirmation system
- **Accessibility First**: WCAG-compliant design with keyboard navigation and screen reader support
- **Responsive Design**: Works seamlessly across desktop, tablet, and mobile devices
- **Privacy Focused**: All processing happens locally in your browser - no data is stored or transmitted

## 🚀 How It Works

1. **Camera Access**: Grant webcam permission to start recognition
2. **Hand Detection**: MediaPipe detects and tracks hand landmarks in real-time
3. **Feature Extraction**: Hand landmarks are processed and normalized
4. **ML Prediction**: Custom-trained model classifies the fingerspelling gesture
5. **Word Building**: Confirmed letters are added to build complete words

## 🛠️ Technical Architecture

### Backend
- **Django**: Robust web framework for API endpoints and template rendering
- **MediaPipe**: Google's hand landmark detection for real-time tracking
- **OpenCV**: Computer vision processing and image manipulation
- **Scikit-learn**: Machine learning model training and inference
- **Custom ML Model**: Trained on ASL fingerspelling dataset with high accuracy

### Frontend
- **Vanilla JavaScript**: Real-time camera feed and prediction handling
- **CSS3**: Modern responsive design with accessibility features
- **WebRTC**: Browser-based camera access without external dependencies

### Model Details
- **Input**: 21 hand landmarks (x, y, z coordinates) from MediaPipe
- **Architecture**: Random Forest classifier optimized for real-time inference
- **Training Data**: Comprehensive ASL fingerspelling dataset
- **Accuracy**: >95% on test dataset with robust performance across different lighting conditions

## 🎨 Design Philosophy

- **Accessibility First**: WCAG 2.1 AA compliant with keyboard navigation and screen reader support
- **Inclusive Design**: High contrast ratios, clear typography, and intuitive interactions
- **Performance**: Optimized for real-time processing with minimal latency
- **Privacy**: No data collection - all processing happens locally

## Screenshots

### Homepage
![Homepage](static/asl.jpg)

### Prediction Page
![Prediction Page](static/detect.png)

## 🔮 Future Roadmap

- **LSF Integration**: Add French Sign Language (LSF) support
- **Learning Modules**: Interactive tutorials and progress tracking
- **Community Features**: User-generated content and practice sessions
- **Full ASL Support**: Expand beyond fingerspelling to complete ASL vocabulary


## 🤝 Why ASL First?

We started with American Sign Language due to the availability of comprehensive datasets. Our long-term vision includes French Sign Language (LSF).

## 📊 Impact & Accessibility

- **Universal Access**: Free tool accessible from any modern web browser
- **Educational**: Supports both deaf and hearing individuals learning ASL
- **Inclusive Technology**: Demonstrates how AI can bridge communication barriers
- **Open Source**: Encouraging community contributions and improvements

## Contributing

Contributions are welcome! Feel free to fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## 📞 Get Involved

Interested in contributing, collaborating, or learning more about the project?

- **Email**: [maximemartin510@gmail.com](mailto:maximemartin510@gmail.com)
- **LinkedIn**: [Maxime Martin](https://www.linkedin.com/in/maxime-martin-090731aa/)

### For Developers
Interested in the technical implementation or want to contribute? Contact me for access to the trained model and detailed documentation.

### For Educators & Researchers
Looking to integrate this technology into educational programs or research projects? Let's discuss collaboration opportunities.

### For the Deaf Community
Your feedback is invaluable in making this tool more effective and inclusive. Please reach out with suggestions and insights.

---

**Signéo** - Making sign language accessible through technology. Together, we're building bridges across communication barriers. 🤟
