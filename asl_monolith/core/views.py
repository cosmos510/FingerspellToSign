import pickle
import numpy as np
import os
from django.conf import settings
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

try:
    import cv2
    CV2_AVAILABLE = True
except ImportError as e:
    print(f"OpenCV not available: {e}")
    CV2_AVAILABLE = False

try:
    import mediapipe as mp
    MEDIAPIPE_AVAILABLE = True
except ImportError as e:
    print(f"Mediapipe not available: {e}")
    MEDIAPIPE_AVAILABLE = False

_cached_hands = None

def get_hands_detector():
    global _cached_hands
    if _cached_hands is None and MEDIAPIPE_AVAILABLE:
        mp_hands = mp.solutions.hands
        _cached_hands = mp_hands.Hands(
            static_image_mode=True,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        print("✅ Hands detector initialized")
    return _cached_hands

global_predicted_character = "No prediction"
_cached_model = None

def load_model():
    global _cached_model
    if _cached_model is None:
        model_path = os.path.join(settings.BASE_DIR, 'model1.p')
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at {model_path}")
        with open(model_path, 'rb') as f:
            model_dict = pickle.load(f)
        _cached_model = model_dict['model']
        print("✅ Model loaded and cached")
    return _cached_model

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
        try:
            if not CV2_AVAILABLE:
                return JsonResponse({'status': 'failed', 'error': 'Image processing not available'}, status=500)
            
            if not MEDIAPIPE_AVAILABLE:
                return JsonResponse({'status': 'failed', 'error': 'Hand detection not available'}, status=500)
                
            if 'file' not in request.FILES:
                return JsonResponse({'status': 'failed', 'error': 'No file part'}, status=400)
            
            file = request.FILES['file']
            if file.size == 0:
                return JsonResponse({'status': 'failed', 'error': 'Empty file'}, status=400)
            
            image = file.read()
            np_arr = np.frombuffer(image, np.uint8)
            img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            
            # Resize image to reduce memory usage
            frame_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            hands = get_hands_detector()
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
                    model = load_model()
                    prediction = model.predict(data_aux_np)
                    global_predicted_character = prediction[0]
            else:
                global_predicted_character = "No hand detected"
                
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Error in upload_frame: {error_msg}")
            print(f"❌ Error type: {type(e).__name__}")
            import traceback
            traceback.print_exc()
            
            # Return more specific error for debugging
            return JsonResponse({
                'status': 'failed', 
                'error': f'Processing error: {error_msg}',
                'error_type': type(e).__name__
            }, status=500)
        
        return JsonResponse({'prediction': global_predicted_character})
    
    return JsonResponse({'status': 'failed', 'error': 'Invalid request method'}, status=400)

def get_prediction(request):
    global global_predicted_character
    return JsonResponse({'prediction': global_predicted_character})

def video_feed(request):
    if not CV2_AVAILABLE:
        return JsonResponse({'error': 'Video feed not available'}, status=500)
        
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

'''
import cv2
import pickle
import numpy as np
import mediapipe as mp
import os
from django.conf import settings
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
global_predicted_character = "No prediction"

model = None

def load_model():
    global model
    if model is None:
        model_path = os.path.join(settings.BASE_DIR, 'model1.p')
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at {model_path}")
        with open(model_path, 'rb') as f:
            model_dict = pickle.load(f)
        model = model_dict['model']

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
        try:
            if 'file' not in request.FILES:
                return JsonResponse({'status': 'failed', 'error': 'No file part'}, status=400)
            
            file = request.FILES['file']
            if file.size == 0:
                return JsonResponse({'status': 'failed', 'error': 'Empty file'}, status=400)
            
            try:
                load_model()
            except FileNotFoundError as e:
                return JsonResponse({'status': 'failed', 'error': str(e)}, status=500)
            
            image = file.read()
            np_arr = np.frombuffer(image, np.uint8)
            img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            frame_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = hands.process(frame_rgb)
        except Exception as e:
            print(f"❌ Error in upload_frame: {str(e)}")
            import traceback
            traceback.print_exc()
            return JsonResponse({'status': 'failed', 'error': f'Processing error: {str(e)}'}, status=500)
            
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

'''