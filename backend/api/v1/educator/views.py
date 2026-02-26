from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status
from course.models import Course
from .serializers import CourseSerializer

class IsEducator(permissions.BasePermission):
    """
    Allows access only to educators.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and getattr(request.user, 'is_educator', False))

class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [IsEducator]
    
    def get_queryset(self):
        # Allow educators to see and manage only their courses
        return Course.objects.filter(provider_user=self.request.user)
        
    def perform_create(self, serializer):
        # Automatically assign the current educator to the course
        serializer.save(provider_user=self.request.user)
