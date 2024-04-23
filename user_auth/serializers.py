from wsgiref import validate
from rest_framework import serializers
from .models import HospitalUser as User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    password2 = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['first_name','last_name','email', 'username', 'password', 'password2', 'gender']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        first_name = attrs.get('first_name', '')
        last_name = attrs.get('last_name', '')

        if (not username.isalnum()
            or not first_name.isalnum()
            or not last_name.isalnum()
        ):
            raise serializers.ValidationError(
                self.default_error_messages)
        
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        
        return attrs
    
    def create(self, validated_data):
        print("validated_data", validated_data)
        return User.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
            email=validated_data['email'],
            gender=validated_data['gender'],
        )
    

class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6,write_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(username=obj['username'])
        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }
    
    class Meta:
        model = User
        fields = ['password','username','tokens']

    def validate(self, attrs):
        username = attrs.get('username','')
        password = attrs.get('password','')
        user = auth.authenticate(username=username,password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs
    
    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')




# "tokens": {
#         "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxMjg4NTQzMywiaWF0IjoxNzEyNzk5MDMzLCJqdGkiOiIwYTYwODdkZGViNjQ0N2JmYmJlZDYzYmNjNmIzYjM0MyIsInVzZXJfaWQiOjN9.0oiOl-xx4dyo-mQ3eJI62dv_eF2Ewh-Sp138Z7FI2G4",
#         "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzEyNzk5MDkzLCJpYXQiOjE3MTI3OTkwMzMsImp0aSI6IjA3MDRiNzdjOTY3YTQ3N2M5MjU2ODMyNzA1MDUyZGQ4IiwidXNlcl9pZCI6M30.1VcDH2MmX2K6H9sR_24xbHKy4BEhgC0VoUCFEaT5AuA"
#     }