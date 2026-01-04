import pickle
import numpy as np
import os
import logging
import sys
from django.conf import settings
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)

try:
    import cv2
    CV2_AVAILABLE = True
    print(f"✅ OpenCV version: {cv2.__version__}")
except ImportError as e:
    print(f"❌ OpenCV not available: {e}")
    CV2_AVAILABLE = False
    # Fallback: utiliser PIL pour le décodage d'images
    try:
        from PIL import Image
        import io
        PIL_AVAILABLE = True
        print("✅ PIL available as fallback")
    except ImportError:
        PIL_AVAILABLE = False
        print("❌ PIL also not available")
except Exception as e:
    print(f"❌ OpenCV error: {e}")
    CV2_AVAILABLE = False
    PIL_AVAILABLE = False

try:
    import mediapipe as mp
    MEDIAPIPE_AVAILABLE = True
    print(f"✅ MediaPipe version: {mp.__version__}")
except ImportError as e:
    print(f"❌ MediaPipe not available: {e}")
    MEDIAPIPE_AVAILABLE = False
except Exception as e:
    print(f"❌ MediaPipe error: {e}")
    MEDIAPIPE_AVAILABLE = False

_cached_hands = None

def get_hands_detector():
    global _cached_hands
    if _cached_hands is None and MEDIAPIPE_AVAILABLE:
        try:
            # Nouvelle API MediaPipe
            from mediapipe.tasks import python
            from mediapipe.tasks.python import vision
            
            base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
            options = vision.HandLandmarkerOptions(base_options=base_options,
                                                 num_hands=1)
            _cached_hands = vision.HandLandmarker.create_from_options(options)
            print("✅ Hands detector initialized (new API)")
        except Exception as e:
            try:
                # Ancienne API MediaPipe (fallback)
                mp_hands = mp.solutions.hands
                _cached_hands = mp_hands.Hands(
                    static_image_mode=True,
                    max_num_hands=1,
                    min_detection_confidence=0.5,
                    min_tracking_confidence=0.5
                )
                print("✅ Hands detector initialized (legacy API)")
            except Exception as e2:
                print(f"❌ Failed to initialize hands detector: {e2}")
                _cached_hands = None
    return _cached_hands

global_predicted_character = "No prediction"
_cached_model = None

def extract_advanced_features(landmarks):
    """Extraction de features avancées - doit générer exactement 87 features"""
    try:
        wrist_x, wrist_y, wrist_z = landmarks[0].x, landmarks[0].y, landmarks[0].z
        coords = []
        for lm in landmarks:
            coords.extend([lm.x, lm.y, lm.z])
        
        normalized_features = []
        for lm in landmarks:
            normalized_features.extend([
                lm.x - wrist_x,
                lm.y - wrist_y, 
                lm.z - wrist_z
            ])
        
        distances = []
        key_points = [(4, 8), (8, 12), (12, 16), (16, 20), (4, 12), (4, 16), (4, 20), (0, 9), (0, 17)]
        
        for p1, p2 in key_points:
            dist = np.sqrt(
                (landmarks[p1].x - landmarks[p2].x)**2 + 
                (landmarks[p1].y - landmarks[p2].y)**2 + 
                (landmarks[p1].z - landmarks[p2].z)**2
            )
            distances.append(dist)
        
        angles = []
        finger_tips = [4, 8, 12, 16, 20]
        finger_bases = [2, 5, 9, 13, 17]
        
        for i in range(len(finger_tips)):
            for j in range(i+1, len(finger_tips)):
                tip1, tip2 = finger_tips[i], finger_tips[j]
                base1, base2 = finger_bases[i], finger_bases[j]
                
                v1 = np.array([landmarks[tip1].x - landmarks[base1].x, landmarks[tip1].y - landmarks[base1].y])
                v2 = np.array([landmarks[tip2].x - landmarks[base2].x, landmarks[tip2].y - landmarks[base2].y])
                
                cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-8)
                angle = np.arccos(np.clip(cos_angle, -1, 1))
                angles.append(angle)
        
        curvatures = []
        fingers = [[1,2,3,4], [5,6,7,8], [9,10,11,12], [13,14,15,16], [17,18,19,20]]
        
        for finger in fingers:
            if len(finger) >= 3:
                p1 = np.array([landmarks[finger[0]].x, landmarks[finger[0]].y])
                p2 = np.array([landmarks[finger[1]].x, landmarks[finger[1]].y])
                p3 = np.array([landmarks[finger[2]].x, landmarks[finger[2]].y])
                
                v1 = p2 - p1
                v2 = p3 - p2
                
                cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-8)
                curvature = np.arccos(np.clip(cos_angle, -1, 1))
                curvatures.append(curvature)
        
        all_features = normalized_features + distances + angles + curvatures
        
        logger.info(f"Generated {len(all_features)} features")
        return all_features
        
    except Exception as e:
        logger.error(f"Feature extraction error: {e}")
        return None

def load_model():
    global _cached_model
    if _cached_model is None:
        model_path = os.path.join(settings.BASE_DIR, 'advanced_asl_model.p')
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Advanced model not found at {model_path}")
        with open(model_path, 'rb') as f:
            model_dict = pickle.load(f)
        _cached_model = model_dict['model']
        print(f"✅ Advanced ASL model loaded - Type: {model_dict.get('model_type', 'Unknown')}")
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
    
    logger.info("upload_frame called")
    
    if request.method != 'POST':
        return JsonResponse({'status': 'failed', 'error': 'Invalid request method'}, status=400)
    
    logger.info(f"CV2_AVAILABLE: {CV2_AVAILABLE}, MEDIAPIPE_AVAILABLE: {MEDIAPIPE_AVAILABLE}")
    
    if not MEDIAPIPE_AVAILABLE:
        return JsonResponse({
            'prediction': 'Service temporarily unavailable - MediaPipe not loaded'
        })
    
    if 'file' not in request.FILES:
        return JsonResponse({'status': 'failed', 'error': 'No file part'}, status=400)
    
    file = request.FILES['file']
    if file.size == 0 or file.size > 200 * 1024:
        return JsonResponse({'status': 'failed', 'error': 'Invalid file size'}, status=400)
    
    try:
        logger.info(f"Processing file size: {file.size} bytes")
        image_data = file.read()
        
        # Décodage d'image avec fallback
        if CV2_AVAILABLE:
            np_arr = np.frombuffer(image_data, np.uint8)
            img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            if img is None:
                return JsonResponse({'status': 'failed', 'error': 'Invalid image'}, status=400)
            frame_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        elif 'PIL_AVAILABLE' in globals() and PIL_AVAILABLE:
            from PIL import Image
            import io
            img_pil = Image.open(io.BytesIO(image_data))
            frame_rgb = np.array(img_pil.convert('RGB'))
        else:
            return JsonResponse({
                'prediction': 'Image processing not available - OpenCV and PIL missing'
            })
        
        hands = get_hands_detector()
        if hands is None:
            return JsonResponse({'prediction': 'MediaPipe detector not available'})
        
        logger.info(f"Processing image shape: {frame_rgb.shape}")
        
        try:
            # Nouvelle API MediaPipe
            import mediapipe as mp
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
            detection_result = hands.detect(mp_image)
            
            if detection_result.hand_landmarks:
                landmarks = detection_result.hand_landmarks[0]
        except Exception as e:
            # Ancienne API MediaPipe (fallback)
            try:
                results = hands.process(frame_rgb)
                if results.multi_hand_landmarks:
                    landmarks = results.multi_hand_landmarks[0].landmark
                else:
                    landmarks = None
            except Exception as e2:
                logger.error(f"Both MediaPipe APIs failed: {e}, {e2}")
                return JsonResponse({'prediction': 'MediaPipe processing failed'})
        
        if 'landmarks' in locals() and landmarks:
            features = extract_advanced_features(landmarks)
            
            if features:
                prediction_input = np.array(features, dtype=np.float32).reshape(1, -1)
                model = load_model()
                prediction = model.predict(prediction_input)
                global_predicted_character = prediction[0]
        else:
            global_predicted_character = "No hand detected"
            
    except Exception as e:
        import traceback
        error_msg = str(e)
        logger.error(f"Error in upload_frame: {error_msg}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return JsonResponse({
            'status': 'failed', 
            'error': f'Processing error: {error_msg}'
        }, status=500)
    
    return JsonResponse({'prediction': global_predicted_character})

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

def rgpd(request):
    return render(request, 'rgpd.html')

def mentions_legales(request):
    return render(request, 'mentions-legales.html')

def sitemap(request):
    return render(request, 'sitemap.xml', content_type='application/xml')

def robots(request):
    from django.http import HttpResponse
    from django.conf import settings
    import os
    
    robots_path = os.path.join(settings.BASE_DIR, 'static', 'robots.txt')
    try:
        with open(robots_path, 'r') as f:
            content = f.read()
        return HttpResponse(content, content_type='text/plain')
    except FileNotFoundError:
        return HttpResponse('User-agent: *\nAllow: /', content_type='text/plain')

def serve_static_file(request, filename):
    """Sert les fichiers statiques avec headers CSP"""
    from django.http import HttpResponse, Http404
    from django.conf import settings
    import os
    import mimetypes
    
    file_path = os.path.join(settings.BASE_DIR, 'static', filename)
    
    if not os.path.exists(file_path):
        raise Http404("File not found")
    
    # Déterminer le type MIME
    content_type, _ = mimetypes.guess_type(file_path)
    if not content_type:
        content_type = 'application/octet-stream'
    
    # Lire le fichier
    with open(file_path, 'rb') as f:
        content = f.read()
    
    response = HttpResponse(content, content_type=content_type)
    
    # Ajouter les headers de sécurité
    response['X-Frame-Options'] = 'SAMEORIGIN'
    response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    
    # CSP spécifique selon le type de fichier
    if filename.endswith('.js'):
        response['Content-Security-Policy'] = "default-src 'none'; script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com;"
    elif filename.endswith('.css'):
        response['Content-Security-Policy'] = "default-src 'none'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com;"
    else:
        response['Content-Security-Policy'] = "default-src 'self';"
    
    return response