from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('predict/', views.predict, name='predict'),
    path('about/', views.about, name='about'),
    path('video_feed/', views.video_feed, name='video_feed'),
    path('get_prediction/', views.get_prediction, name='get_prediction'),
    path('upload_frame/', views.upload_frame, name='upload_frame'),
    path('rgpd/', views.rgpd, name='rgpd'),
    path('mentions-legales/', views.mentions_legales, name='mentions_legales'),
    path('sitemap.xml', views.sitemap, name='sitemap'),
    path('robots.txt', views.robots, name='robots'),
    # Fichiers statiques avec headers CSP
    path('static/asl.jpg', views.serve_static_file, {'filename': 'asl.jpg'}, name='static_asl_jpg'),
    path('static/profile.png', views.serve_static_file, {'filename': 'profile.png'}, name='static_profile_png'),
    path('static/three-bg.js', views.serve_static_file, {'filename': 'three-bg.js'}, name='static_three_bg_js'),
    path('static/index.css', views.serve_static_file, {'filename': 'index.css'}, name='static_index_css'),
    path('static/predict.js', views.serve_static_file, {'filename': 'predict.js'}, name='static_predict_js'),
    path('static/predict.css', views.serve_static_file, {'filename': 'predict.css'}, name='static_predict_css'),
]