from django.urls import path

""" TokenObtainPairView: Genera la pareja de tokens refresh, access
    TokenRefreshView: a partir del token de refresh genera un token de acces"""
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from authApp import admin, views
from django.contrib import admin
urlpatterns = [
    path('admin/', admin.site.urls),
    # Login - Cada vez que un usuario se logue se les genera un token de refresh(24 horas) y un primer token de acceso(5 minutos) 
    path('login/',         TokenObtainPairView.as_view()), 
    # refresh - Se recibe como parametro un token de refresh para generar un nuevo token de acceso
    path('refresh/',       TokenRefreshView.as_view()),
    path('user/',          views.UserCreateView.as_view()), # vista creada en el proyecto para la creacion de un usuario
    path('user/<int:pk>/', views.UserDetailView.as_view()), # vista creada en el proyecto para consultar un usuario
]