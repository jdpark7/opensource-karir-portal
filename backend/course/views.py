from django.shortcuts import render
from django.db.models import Q
from .models import Course
from peeldb.models import Company
from django.core.paginator import Paginator

def course_list(request):
    query = request.GET.get('q', '').strip()
    provider = request.GET.get('provider', '').strip()

    # Get distinct providers for the dropdown
    provider_ids = Course.objects.filter(status='Active').exclude(provider__isnull=True).values_list('provider', flat=True).distinct()
    providers = Company.objects.filter(id__in=provider_ids).order_by('name')

    courses = Course.objects.filter(status='Active')
    
    is_search = False

    if query:
        courses = courses.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(keywords__icontains=query) |
            Q(skills__icontains=query)
        )
        is_search = True
        
    if provider:
        courses = courses.filter(provider=provider)
        is_search = True

    if is_search:
        courses = courses.order_by('-created_at')
        
        paginator = Paginator(courses, 12) # Show 12 courses per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    else:
        courses_list = list(courses.order_by('?')[:12])
        paginator = Paginator(courses_list, 12)
        page_obj = paginator.get_page(1)

    context = {
        'page_obj': page_obj,
        'query': query,
        'providers': providers,
        'selected_provider': provider,
    }
    return render(request, 'course/course_list.html', context)
