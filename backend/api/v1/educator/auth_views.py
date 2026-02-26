"""
Authentication views for Educator users.

Provides a `login` endpoint similar to recruiter auth but scoped to `ED` user_type.
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema

from django.contrib.auth import authenticate
from peeldb.models import User


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@extend_schema(
    tags=["Educator Auth"],
    summary="Login (Educator)",
    description="Authenticate educator user and return JWT tokens",
    request={
        'type': 'object',
        'properties': {
            'email': {'type': 'string'},
            'password': {'type': 'string'}
        },
        'required': ['email', 'password']
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    # Validate input
    email = (request.data.get('email') or '').lower()
    password = request.data.get('password')

    if not email or not password:
        return Response({'detail': 'Must provide email and password'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=email, password=password)
    if not user:
        return Response({'detail': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)

    if user.user_type != 'ED':
        return Response({'detail': 'This email is not registered as an educator. Please use the appropriate login.'}, status=status.HTTP_400_BAD_REQUEST)

    if not user.is_active:
        return Response({'detail': 'Please verify your email address first.'}, status=status.HTTP_400_BAD_REQUEST)

    tokens = get_tokens_for_user(user)

    # Minimal user data
    user_data = {
        'id': user.id,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'user_type': user.user_type,
    }

    return Response({
        'access': tokens['access'],
        'refresh': tokens['refresh'],
        'user': user_data
    })
