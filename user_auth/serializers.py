from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate

from core.models import Patient
from .models import DoctorProfile, PatientProfile

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class DoctorRegistrationSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = DoctorProfile
        fields = ('user', 'specialty')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        user.is_doctor = True
        user.save()
        doctor_profile = DoctorProfile.objects.create(user=user, **validated_data)
        return doctor_profile

class PatientRegistrationSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = PatientProfile
        fields = ('user', 'condition')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        user.is_patient = True
        user.save()
        patient_profile = PatientProfile.objects.create(user=user, **validated_data)
        return patient_profile

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")
