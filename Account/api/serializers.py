from django.contrib.auth import get_user_model
from dj_rest_auth.serializers import LoginSerializer
from rest_framework import serializers
from ..models import Profile


class UserListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='Account:user_detail')

    class Meta:
        model = get_user_model()
        fields = [
            'url',
            'id', 'username',
            'email', 'phone',
        ]


class UserDetailSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='Account:user_profile')

    class Meta:
        model = get_user_model()
        fields = [
            'url', 'id',
            'username', 'email',
            'phone', 'date_joined',
            'last_update', 'last_login',
        ]
        extra_kwargs = {
            'phone': {'required': True}
        }


class ProfileUserSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(source='user.username')

    class Meta:
        model = Profile
        fields = '__all__'


class AuthLoginSerializer(LoginSerializer):
    username = serializers.CharField(required=True, allow_blank=True)
    email = serializers.EmailField(read_only=True, allow_blank=True)
    password = serializers.CharField(style={'input_type': 'password'})
