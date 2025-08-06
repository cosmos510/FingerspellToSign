import cv2
import pickle
import numpy as np
import mediapipe as mp
import os
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Load ML model
model_path = os.path.join(settings.BASE_DIR, 'model1.p')
model_dict = pickle.load(open(model_path, 'rb'))
model = model_dict['model']

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
global_predicted_character = "No prediction"

def home(request):
    return render(request, 'index.html')

def predict(request):
    return render(request, 'predict.html')

def about(request):
    return render(request, 'about.html')

@csrf_exempt
def upload_frame(request):
    global global_predicted_character
    
    if request.method == 'POST':
        if 'file' not in request.FILES:
            return JsonResponse({'status': 'failed', 'error': 'No file part'}, status=400)
        
        file = request.FILES['file']
        if file.size == 0:
            return JsonResponse({'status': 'failed', 'error': 'Empty file'}, status=400)
        
        image = file.read()
        np_arr = np.frombuffer(image, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        frame_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)
        
        if results.multi_hand_landmarks:
            data_aux = []
            x_ = []
            y_ = []
            
            hand_landmarks = results.multi_hand_landmarks[0]
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                x_.append(x)
                y_.append(y)
            
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                data_aux.append(x - min(x_))
                data_aux.append(y - min(y_))
            
            if len(data_aux) == 42:
                data_aux_np = np.array(data_aux).reshape(1, -1)
                prediction = model.predict(data_aux_np)
                global_predicted_character = prediction[0]
        else:
            global_predicted_character = "No hand detected"
        
        return JsonResponse({'prediction': global_predicted_character})
    
    return JsonResponse({'status': 'failed', 'error': 'Invalid request method'}, status=400)

def get_prediction(request):
    global global_predicted_character
    return JsonResponse({'prediction': global_predicted_character})

def video_feed(request):
    def generate():
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                continue
            ret, jpeg = cv2.imencode('.jpg', frame)
            frame = jpeg.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    
    return StreamingHttpResponse(generate(), content_type='multipart/x-mixed-replace; boundary=frame')



def header_view(request):
    return render(request, 'header.html')

def footer_view(request):
    return render(request, 'footer.html')