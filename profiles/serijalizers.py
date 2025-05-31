from rest_framework import serializers
from .models import Profile # moj model koji sam kreirao
from django.contrib.auth.models import User # koristim za registraciju korisnika
from django.contrib.auth.password_validation import validate_password # koristim za validaciju passworda

# registracijski serijalizer za korisnika
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2']


    # provjera passworda 1 i 2
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Lozinke se ne poklapaju.")
        return data
    
    # proverava da li je lozinka dovoljno jaka i složena prema pravilima
    def validate_password(self, value):
        validate_password(value)
        return value
    
    # sprema korisnika u bazu
    def create(self, validated_data):
        validated_data.pop('password2') # uklanjam password2 iz validiranih podataka
        user = User.objects.create_user(**validated_data)
        return user

# update seriijalizer
class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']