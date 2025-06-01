from django.shortcuts import render
from rest_framework.views import APIView
from  rest_framework.response import Response
from rest_framework import status
from .serijalizers import RegisterSerializer, UpdateUserSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated # za authntifikaciju korisnika
from django.contrib.auth.tokens import default_token_generator #generiše token za verifikaciju korisnika
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode #  Kodira i dekodira korisnikov ID (npr. user.pk) da bude siguran za URL.
from django.utils.encoding import force_bytes # Pretvara string ili broj u bajtove pre base64 kodiranja.
from django.core.mail import send_mail # Šalje mejl pomoću Django-ovog email backend sistema.
from django.conf import settings # Omogućava pristup Django konfiguracijama (iz settings.py).
from django.utils.encoding import force_str # funkcija iz Django biblioteke koja pretvara bilo koji objekat u Python str (string) 
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer # serializer iz SimpleJWT biblioteke koji se koristi za dobijanje JWT tokena
from rest_framework.exceptions import AuthenticationFailed #  izuzetak (exception) koji se koristi kada autentikacija ne uspe 
from rest_framework_simplejwt.views import TokenObtainPairView # gotova DRF view klasa koja koristi TokenObtainPairSerializer da bi omogućila login korisnika i generisanje tokena.

# login
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        if not self.user.is_active:
            raise AuthenticationFailed('Email nije verifikovan. Aktiviraj nalog.')

        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# klasa za unos novog korisnika
class RegisterView(APIView):
    def post(self, request, format=None):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # generiši token i uid
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            verification_link = f"http://127.0.0.1:8000/profiles/verify-email/{uid}/{token}/"

            # pošalji email
            send_mail(
                'Verifikuj svoj nalog',
                f'Klikni na link da aktiviraš nalog: {verification_link}',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# kreiranje klsase za verifikaciju emaila
class VerifyEmailView(APIView):
    def get(self, request, uid, token):
        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'error': 'Nevažeći link.'}, status=400)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({'message': 'Email je uspešno verifikovan.'}, status=200)
        else:
            return Response({'error': 'Token nije validan ili je istekao.'}, status=400)



# prikaz detalja korisnika brisanje i ažuriranje
class RegisterDetailWiew(APIView):
    #permission_classes = [IsAuthenticated] # samo prijavljeni korisnici mogu pristupiti ovoj klasi
    
    # prikaz detalja korisnika
    def get(self, request, pk, format=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UpdateUserSerializer(user)
        return Response(serializer.data)
    
    # ažuriranje korisnika
    def put(self, request, pk, format=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UpdateUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # brisanje korisnika
    def delete(self, request, pk, format=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
