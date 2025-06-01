from django.urls import path
from . import views

# uvoz jwt za login i logout
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    #registracija korisnika
    path('register/', views.RegisterView.as_view(), name='register'),
    path('register/<int:pk>/', views.RegisterDetailWiew.as_view(), name='register-detail'),

    # login i refresh token
    path('login/', views.CustomTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('verify-email/<uid>/<token>/', views.VerifyEmailView.as_view(), name='verify-email'), # verifikacija maila
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'), # promjena lozinke

]