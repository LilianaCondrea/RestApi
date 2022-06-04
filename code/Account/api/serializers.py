from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from dj_rest_auth.serializers import LoginSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
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


class AuthRegisterSerializer(RegisterSerializer):
    phone = serializers.CharField(required=True, write_only=True, allow_blank=True, max_length=15)

    def validate_phone(self, value):
        user = get_user_model().objects.filter(phone=value)
        if not value.isdigit():
            raise serializers.ValidationError('Phone number must be numeric.')
        elif user.exists():
            raise serializers.ValidationError('Phone number already exists with another user.')
        return value

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'phone': self.validated_data.get('phone', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user = adapter.save_user(request, user, self, commit=False)
        if "password1" in self.cleaned_data:
            try:
                adapter.clean_password(self.cleaned_data['password1'], user=user)
            except DjangoValidationError as exc:
                raise serializers.ValidationError(
                    detail=serializers.as_serializer_error(exc)
                )
        user.phone = self.cleaned_data['phone']
        user.save()
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user
