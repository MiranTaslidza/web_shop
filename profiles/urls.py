from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('register/<int:pk>/', views.RegisterDetailWiew.as_view(), name='register-detail'),

]