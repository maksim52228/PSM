from . import views
from .views import  works
from django_otp.admin import OTPAdminSite
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import team_view
from django.contrib import admin
from django.urls import path, include






urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('chat/', views.chat, name='chat'),
    path('news/', views.news_list, name='news_list'),  
    path('news/<int:pk>/', views.news_detail, name='news_detail'),
    path('set_chat_username/', views.set_chat_username, name='set_chat_username'),
    path('team/', team_view, name='team'),
    path('works/', works, name='works'),
    path('send-admin-message/', views.send_admin_message, name='send_admin_message'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)