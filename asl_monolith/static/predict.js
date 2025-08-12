async function setupWebcam() {
    const webcamElement = document.getElementById('webcam');
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        webcamElement.srcObject = stream;
    } catch (err) {
        console.error('Webcam access error');
        document.getElementById('prediction-text').innerText = 'Webcam access denied. Please allow camera access.';
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function sendFrameToServer(blob) {
    if (!(blob instanceof Blob)) {
        console.error('Invalid blob data');
        return;
    }

    const formData = new FormData();
    formData.append('file', blob, 'frame.jpg');

    fetch("/upload_frame/", {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        const prediction = data.prediction || 'No prediction';
        updatePredictionDisplay(prediction);
    })
    .catch(error => {
        console.error('Request failed');
        updatePredictionDisplay('Error processing frame');
    });
}

let reusableCanvas = null;

function captureFrame() {
    try {
        const videoElement = document.getElementById('webcam');
        if (!videoElement || videoElement.videoWidth === 0) {
            return;
        }
        
        if (!reusableCanvas) {
            reusableCanvas = document.createElement('canvas');
        }
        
        const maxWidth = 160;
        const maxHeight = 120;
        const videoWidth = videoElement.videoWidth;
        const videoHeight = videoElement.videoHeight;
        
        let canvasWidth = videoWidth;
        let canvasHeight = videoHeight;
        
        if (videoWidth > maxWidth || videoHeight > maxHeight) {
            const scale = Math.min(maxWidth / videoWidth, maxHeight / videoHeight);
            canvasWidth = Math.floor(videoWidth * scale);
            canvasHeight = Math.floor(videoHeight * scale);
        }
        
        reusableCanvas.width = canvasWidth;
        reusableCanvas.height = canvasHeight;
        
        const context = reusableCanvas.getContext('2d');
        context.drawImage(videoElement, 0, 0, canvasWidth, canvasHeight);
        
        if (reusableCanvas.toBlob) {
            reusableCanvas.toBlob(blob => {
                if (blob) {
                    sendFrameToServer(blob);
                }
            }, 'image/jpeg', 0.3);
        }
    } catch (error) {
        console.error('Frame capture failed');
    }
}

function addLetterToWord() {
    const predictedLetter = document.getElementById('prediction-text').innerText;
    const currentWordElement = document.getElementById('current-word');
    if (predictedLetter.trim() === 'space') {
        currentWordElement.innerText += ' '; 
    } else if (predictedLetter && predictedLetter !== 'No hand detected') {
        currentWordElement.innerText += predictedLetter;
    } else {
        updatePredictionDisplay('No valid hand detected. Please ensure your hand is visible to the camera.');
    }
}

function updatePredictionDisplay(prediction) {
    const predictionElement = document.getElementById('prediction-text');
    
    if (prediction === 'del' || prediction === 'space') {
        predictionElement.classList.add('hidden');
    } else if (prediction === 'No hand detected' || prediction.toLowerCase().includes('no hand')) {
        predictionElement.classList.remove('hidden');
        predictionElement.classList.add('no-hand');
        predictionElement.textContent = prediction;
    } else {
        predictionElement.classList.remove('hidden', 'no-hand');
        predictionElement.textContent = prediction;
    }
}
function clearWord() {
    document.getElementById('current-word').innerText = '';
}

document.addEventListener("DOMContentLoaded", function() {
    document.getElementById('confirm-letter').addEventListener('click', addLetterToWord);
    document.getElementById('clear-word').addEventListener('click', clearWord);
    
    setupWebcam();
    setInterval(captureFrame, 2000);
});