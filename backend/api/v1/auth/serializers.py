"""
Authentication Serializers for Job Seekers
"""
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.crypto import get_random_string
from peeldb.models import User, Google


class RegisterSerializer(serializers.Serializer):
    """
    Registration serializer for new Job Seeker accounts
    """
    # Personal Info
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100, required=False, allow_blank=True)
    email = serializers.EmailField()

    # Account Security
    password = serializers.CharField(min_length=8, write_only=True)
    confirm_password = serializers.CharField(min_length=8, write_only=True)

    def validate_email(self, value):
        """Check if email already exists"""
        if User.objects.filter(email=value.lower()).exists():
            raise serializers.ValidationError("A user with this email already exists")
        return value.lower()

    def validate(self, data):
        """Cross-field validation"""
        # Check passwords match
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match"})

        # Validate password strength
        try:
            validate_password(data['password'])
        except DjangoValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        return data

    def create(self, validated_data):
        """Create job seeker user"""
        email = validated_data['email']

        # Parse full name into first/last name
        first_name = validated_data.get('first_name', '')
        last_name = validated_data.get('last_name', '')

        # Generate username from email
        username = email.split('@')[0] + '_' + get_random_string(6)

        # Generate activation code for email verification
        activation_code = get_random_string(32)

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=validated_data['password'],
            user_type='JS',  # Job Seeker
            is_active=False,  # Requires email verification
            email_verified=False,
            activation_code=activation_code
        )

        return {
            'user': user,
            'activation_code': activation_code
        }


class VerifyEmailSerializer(serializers.Serializer):
    """Serializer for email verification"""
    token = serializers.CharField(required=True)

    def validate_token(self, value):
        """Validate token and find user"""
        try:
            user = User.objects.get(activation_code=value, is_active=False)
            self.user = user
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid or expired verification token")


class ResendVerificationSerializer(serializers.Serializer):
    """Serializer for resending verification email"""
    email = serializers.EmailField()

    def validate_email(self, value):
        """Check if user exists and is not verified"""
        email = value.lower()
        try:
            user = User.objects.get(email=email, is_active=False, user_type='JS')
            self.user = user
            return email
        except User.DoesNotExist:
            raise serializers.ValidationError("No unverified account found with this email")


class ForgotPasswordSerializer(serializers.Serializer):
    """Serializer for forgot password request"""
    email = serializers.EmailField()

    def validate_email(self, value):
        """Check if user exists"""
        email = value.lower()
        try:
            user = User.objects.get(email=email, user_type='JS')
            self.user = user
            return email
        except User.DoesNotExist:
            # Don't reveal if email exists or not for security
            return email


class ResetPasswordSerializer(serializers.Serializer):
    """Serializer for password reset"""
    token = serializers.CharField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)
    confirm_password = serializers.CharField(min_length=8, write_only=True)

    def validate_token(self, value):
        """Validate reset token"""
        try:
            user = User.objects.get(activation_code=value, user_type='JS')
            self.user = user
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid or expired reset token")

    def validate(self, data):
        """Cross-field validation"""
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match"})

        try:
            validate_password(data['password'])
        except DjangoValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        return data


class LoginSerializer(serializers.Serializer):
    """Login serializer for Job Seekers"""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    remember_me = serializers.BooleanField(default=False)

    def validate(self, data):
        """Authenticate user"""
        email = data.get('email', '').lower()
        password = data.get('password')

        if email and password:
            user = authenticate(username=email, password=password)

            if user:
                # Check if user is job seeker type
                if user.user_type != 'JS':
                    raise serializers.ValidationError(
                        "This email is registered as an employer. Please use the employer login."
                    )

                # Check if email is verified
                if not user.is_active:
                    raise serializers.ValidationError(
                        "Please verify your email address first. Check your inbox for the verification link."
                    )

                data['user'] = user
            else:
                raise serializers.ValidationError("Invalid email or password")
        else:
            raise serializers.ValidationError("Must provide email and password")

        return data


class GoogleAuthSerializer(serializers.Serializer):
    """Serializer for Google OAuth callback - Job Seekers only"""

    code = serializers.CharField(
        required=True, help_text="Authorization code from Google OAuth"
    )
    redirect_uri = serializers.URLField(
        required=True, help_text="Frontend callback URL that was registered with Google"
    )


class UserSerializer(serializers.ModelSerializer):
    """Job Seeker user profile serializer"""

    user_type_display = serializers.CharField(
        source="get_user_type_display", read_only=True
    )
    is_gp_connected = serializers.BooleanField(read_only=True)
    profile_completion_percentage = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "user_type",
            "user_type_display",
            "photo",
            "profile_pic",
            "is_gp_connected",
            "profile_completion_percentage",
            "mobile",
            "gender",
            "is_active",
            "date_joined",
        ]
        read_only_fields = ["id", "username", "user_type", "date_joined"]


class GoogleAccountSerializer(serializers.ModelSerializer):
    """Google account connection info"""

    class Meta:
        model = Google
        fields = ["google_id", "name", "email", "picture", "verified_email"]
        read_only_fields = fields


class TokenResponseSerializer(serializers.Serializer):
    """JWT token response for successful authentication"""

    access = serializers.CharField(help_text="JWT access token (expires in 1 hour)")
    refresh = serializers.CharField(help_text="JWT refresh token (expires in 7 days)")
    user = UserSerializer(help_text="Authenticated user profile")
    requires_profile_completion = serializers.BooleanField(
        default=False,
        help_text="Whether user needs to complete their profile (< 50%)",
    )
    redirect_to = serializers.CharField(
        required=False, help_text="Suggested redirect path for frontend"
    )
    is_new_user = serializers.BooleanField(
        default=False, help_text="Whether this is a newly created user"
    )


class RefreshTokenSerializer(serializers.Serializer):
    """Token refresh request"""

    refresh = serializers.CharField(help_text="Refresh token from login")


class GoogleUrlRequestSerializer(serializers.Serializer):
    """Request serializer for Google OAuth URL generation"""

    redirect_uri = serializers.URLField(
        required=True, help_text="Frontend callback URL"
    )


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for password change"""

    old_password = serializers.CharField(
        required=True,
        write_only=True,
        help_text="Current password"
    )
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        min_length=8,
        help_text="New password (minimum 8 characters)"
    )
    confirm_password = serializers.CharField(
        required=True,
        write_only=True,
        help_text="Confirm new password"
    )

    def validate_old_password(self, value):
        """Validate that the old password is correct"""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Current password is incorrect")
        return value

    def validate(self, data):
        """Validate that new passwords match"""
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({
                'confirm_password': "New passwords do not match"
            })

        # Check that new password is different from old
        if data['old_password'] == data['new_password']:
            raise serializers.ValidationError({
                'new_password': "New password must be different from current password"
            })

        return data
