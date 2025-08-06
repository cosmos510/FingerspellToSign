from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('predict/', views.predict, name='predict'),
    path('about/', views.about, name='about'),
    path('video_feed/', views.video_feed, name='video_feed'),
    path('get_prediction/', views.get_prediction, name='get_prediction'),
    path('upload_frame/', views.upload_frame, name='upload_frame'),
    path('header.html', views.header_view, name='header'),
    path('footer.html', views.footer_view, name='footer'),
]