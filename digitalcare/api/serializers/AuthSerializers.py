from rest_framework import serializers
from ..models import User, Otp
from .ProfileSerializers import (
    AdultProfileSerializer, 
    StudentProfileSerializer, 
    VisitorProfileSerializer
)
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



class UserSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'status', 'phone_number', 'profile']

    def get_profile(self, obj):
        if obj.role == User.ADULT and hasattr(obj, 'adultprofile'):
            return AdultProfileSerializer(obj.adultprofile).data
        elif obj.role == User.STUDENT and hasattr(obj, 'studentprofile'):
            return StudentProfileSerializer(obj.studentprofile).data
        elif obj.role == User.VISITOR and hasattr(obj, 'visitorprofile'):
            return VisitorProfileSerializer(obj.visitorprofile).data
        return None

    def create(self, validated_data):
        # User profile creation is handled in signals
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if profile_data:
            if instance.role == User.ADULT and hasattr(instance, 'adultprofile'):
                self._update_profile(instance.adultprofile, profile_data)
            elif instance.role == User.STUDENT and hasattr(instance, 'studentprofile'):
                self._update_profile(instance.studentprofile, profile_data)
            elif instance.role == User.VISITOR and hasattr(instance, 'visitorprofile'):
                self._update_profile(instance.visitorprofile, profile_data)

        return instance

    def _update_profile(self, profile_instance, profile_data):
        for attr, value in profile_data.items():
            setattr(profile_instance, attr, value)
        profile_instance.save()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, required=True)
    latitude = serializers.FloatField(write_only=True, required=False)
    longitude = serializers.FloatField(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'password',
            'password2',
            'role',
            'status',
            'phone_number',
            'latitude',
            'longitude'
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError({"username": "Username already taken."})
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "Email already in use."})
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password2', None)  # Not needed anymore
        latitude = validated_data.pop('latitude', None)
        longitude = validated_data.pop('longitude', None)

        # Create the user and set password
        user = User(**validated_data)
        user.set_password(password)
        user.save()  # profile created via post_save signal

        # Update profile with latitude and longitude
        profile = None
        if user.role == User.ADULT and hasattr(user, 'adultprofile'):
            profile = user.adultprofile
        elif user.role == User.STUDENT and hasattr(user, 'studentprofile'):
            profile = user.studentprofile
        elif user.role == User.VISITOR and hasattr(user, 'visitorprofile'):
            profile = user.visitorprofile

        if profile:
            if latitude is not None:
                profile.latitude = latitude
            if longitude is not None:
                profile.longitude = longitude
            profile.save()

        return user



class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)


class LoginSerializer(TokenObtainPairSerializer): 
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        token['role'] = user.role
        token['status'] = user.status
        token['phone_number'] = user.phone_number
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        # Prevent login if banned
        if user.status == User.BANNED:
            raise serializers.ValidationError("This account has been banned and cannot log in.")

        # OTP verification (skip for superusers and staff)
        if not user.is_superuser and not user.is_staff:
            try:
                otp = Otp.objects.get(user=user)
                if not otp.is_verified:
                    raise serializers.ValidationError(
                        "Email not verified. Please verify your email with the OTP sent to you."
                    )
            except Otp.DoesNotExist:
                raise serializers.ValidationError(
                    "OTP verification is required but no OTP record was found."
                )

        # Extra user info in response
        data['username'] = user.username
        data['email'] = user.email
        data['role'] = user.role
        data['status'] = user.status
        data['phone_number'] = user.phone_number
        return data
