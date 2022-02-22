from rest_framework import serializers
from .models import MyUser


class SignInSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=150)

    class Meta:
        model = MyUser
        fields = ['username', 'password']


class SignUpSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = MyUser
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def save(self):
        user = MyUser(email=self.validated_data['email'],
                      username=self.validated_data['username'])
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Password mismatch !!!'})
        user.set_password(password)
        user.save()
        return user


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=200)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['name', 'email', 'date_of_birth']
