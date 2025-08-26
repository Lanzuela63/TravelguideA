# users/serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        roles = list(user.groups.values_list('name', flat=True))
        data['role'] = roles[0] if roles else "Tourist"  # Default fallback
        return data

class UserRegistrationSerializer(serializers.ModelSerializer):
    role = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'role')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # role = validated_data.pop('role')
        user = User.objects.create_user(**validated_data)
        return user


