"""
Educator Course management views (CRUD + metadata + stats)

These mirror recruiter job views but operate on the `Course` model and
are scoped to `request.user` as the `provider_user`.
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from django.db.models import Q
from django.utils import timezone

from course.models import Course
from .serializers import CourseSerializer


class CoursePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


@extend_schema(
    tags=["Educator - Courses"],
    summary="List Educator's Courses",
    description="Get all courses uploaded by the authenticated educator with filtering",
    parameters=[
        OpenApiParameter('status', OpenApiTypes.STR, description='Filter by status (Active, Inactive)'),
        OpenApiParameter('search', OpenApiTypes.STR, description='Search by name, instructor or provider'),
        OpenApiParameter('ordering', OpenApiTypes.STR, description='Order by field (created_at, -created_at, name)'),
        OpenApiParameter('page', OpenApiTypes.INT, description='Page number'),
        OpenApiParameter('page_size', OpenApiTypes.INT, description='Items per page (max 100)'),
    ],
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_courses(request):
    user = request.user

    # List courses provided by the user's organization
    company = getattr(user, 'company', None)
    queryset = Course.objects.none()
    if company is not None:
        queryset = Course.objects.filter(provider=company)

    status_filter = request.GET.get('status')
    if status_filter:
        queryset = queryset.filter(status=status_filter)

    search = request.GET.get('search')
    if search:
        queryset = queryset.filter(
            Q(name__icontains=search) |
            Q(instructor__icontains=search) |
            Q(provider__name__icontains=search)
        )

    ordering = request.GET.get('ordering', '-created_at')
    queryset = queryset.order_by(ordering)

    paginator = CoursePagination()
    page = paginator.paginate_queryset(queryset, request)

    if page is not None:
        serializer = CourseSerializer(page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)

    serializer = CourseSerializer(queryset, many=True, context={'request': request})
    return Response(serializer.data)


@extend_schema(
    tags=["Educator - Courses"],
    summary="Get Course Details",
    description="Get detailed information about a specific course",
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_course(request, course_id):
    user = request.user
    company = getattr(user, 'company', None)
    try:
        if company is None:
            raise Course.DoesNotExist
        course = Course.objects.get(id=course_id, provider=company)
    except Course.DoesNotExist:
        return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = CourseSerializer(course, context={'request': request})
    return Response(serializer.data)


@extend_schema(
    tags=["Educator - Courses"],
    summary="Create Course",
    description="Create a new course",
    request=CourseSerializer,
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_course(request):
    user = request.user

    # Ensure course is created for the user's company
    company = getattr(user, 'company', None)
    if company is None:
        return Response({"error": "User is not associated with a company."}, status=status.HTTP_400_BAD_REQUEST)

    serializer = CourseSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        course = serializer.save(provider_user=user, provider=company)
        return Response({"success": True, "course": CourseSerializer(course, context={'request': request}).data}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["Educator - Courses"],
    summary="Update Course",
    description="Update an existing course",
    request=CourseSerializer,
)
@api_view(['PATCH', 'PUT'])
@permission_classes([IsAuthenticated])
def update_course(request, course_id):
    user = request.user
    company = getattr(user, 'company', None)
    try:
        if company is None:
            raise Course.DoesNotExist
        course = Course.objects.get(id=course_id, provider=company)
    except Course.DoesNotExist:
        return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = CourseSerializer(course, data=request.data, partial=(request.method == 'PATCH'), context={'request': request})
    if serializer.is_valid():
        # prevent changing provider to a different company by enforcing user's company
        course = serializer.save(provider=company)
        return Response({"success": True, "course": CourseSerializer(course, context={'request': request}).data})

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["Educator - Courses"],
    summary="Delete Course",
    description="Delete an educator's course",
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_course(request, course_id):
    user = request.user
    company = getattr(user, 'company', None)
    try:
        if company is None:
            raise Course.DoesNotExist
        course = Course.objects.get(id=course_id, provider=company)
    except Course.DoesNotExist:
        return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

    course_name = course.name
    course.delete()
    return Response({"success": True, "message": f"Course '{course_name}' deleted"})


@extend_schema(
    tags=["Educator - Courses"],
    summary="Set Course Active/Inactive",
    description="Activate or deactivate a course (POST with action=activate/deactivate)",
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_course_status(request, course_id):
    user = request.user
    company = getattr(user, 'company', None)
    try:
        if company is None:
            raise Course.DoesNotExist
        course = Course.objects.get(id=course_id, provider=company)
    except Course.DoesNotExist:
        return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

    action = request.data.get('action')
    if action == 'activate':
        course.status = 'Active'
    elif action == 'deactivate':
        course.status = 'Inactive'
    else:
        return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)

    course.save()
    return Response({"success": True, "course": CourseSerializer(course, context={'request': request}).data})


@extend_schema(
    tags=["Educator - Courses"],
    summary="Get Course Form Metadata",
    description="Get metadata needed for course creation form",
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_course_form_metadata(request):
    # Minimal metadata — could be extended (providers, common skills, categories)
    skills = []
    # If a Skill model exists, return top skills; otherwise return empty list
    try:
        from peeldb.models import Skill as PeelSkill
        skills_qs = PeelSkill.objects.filter(status='Active').order_by('name')[:100]
        skills = [{'id': s.id, 'name': s.name, 'slug': getattr(s, 'slug', None)} for s in skills_qs]
    except Exception:
        skills = []

    return Response({
        'skills': skills,
    })


@extend_schema(
    tags=["Educator - Courses"],
    summary="Get Dashboard Stats for Educator",
    description="Get counts and recent courses for the authenticated educator",
    parameters=[
        OpenApiParameter('period', OpenApiTypes.STR, description='Time period for trend calculation: 7d, 30d, 90d (default: 30d)'),
    ],
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_dashboard_stats(request):
    user = request.user
    period = request.GET.get('period', '30d')

    if period == '7d':
        days = 7
    elif period == '90d':
        days = 90
    else:
        days = 30

    from datetime import timedelta
    start_date = timezone.now() - timedelta(days=days)

    company = getattr(user, 'company', None)
    courses = Course.objects.none()
    if company is not None:
        courses = Course.objects.filter(provider=company)
    total = courses.count()
    active = courses.filter(status='Active').count()
    inactive = courses.filter(status='Inactive').count()

    recent = courses.order_by('-created_at')[:5]
    recent_data = [CourseSerializer(c, context={'request': request}).data for c in recent]

    new_count = courses.filter(created_at__gte=start_date).count()

    return Response({
        'stats': {
            'total_courses': total,
            'active_courses': active,
            'inactive_courses': inactive,
            'new_in_period': new_count,
        },
        'recent_courses': recent_data,
    })


@extend_schema(
    tags=["Educator - Courses"],
    summary="Bulk actions on courses",
    description="Perform bulk actions (delete / activate / deactivate) on a list of course IDs",
    request={
        'type': 'object',
        'properties': {
            'action': {'type': 'string', 'enum': ['delete', 'activate', 'deactivate']},
            'ids': {'type': 'array', 'items': {'type': 'integer'}}
        },
        'required': ['action', 'ids']
    }
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def bulk_course_action(request):
    """Perform bulk actions on educator's courses"""
    user = request.user
    data = request.data
    action = data.get('action')
    ids = data.get('ids')

    if not action or not isinstance(ids, (list, tuple)):
        return Response({'error': 'Missing or invalid "action" or "ids"'}, status=status.HTTP_400_BAD_REQUEST)

    valid_actions = ('delete', 'activate', 'deactivate')
    if action not in valid_actions:
        return Response({'error': f'Invalid action. Must be one of: {", ".join(valid_actions)}'}, status=status.HTTP_400_BAD_REQUEST)

    results = {'processed': 0, 'errors': []}

    for cid in ids:
        try:
            course = Course.objects.get(id=cid, provider_user=user)
        except Course.DoesNotExist:
            results['errors'].append({'id': cid, 'error': 'not_found_or_no_permission'})
            continue

        try:
            if action == 'delete':
                course.delete()
            elif action == 'activate':
                course.status = 'Active'
                course.save()
            elif action == 'deactivate':
                course.status = 'Inactive'
                course.save()

            results['processed'] += 1
        except Exception as e:
            results['errors'].append({'id': cid, 'error': str(e)})

    return Response({'success': True, 'results': results})
