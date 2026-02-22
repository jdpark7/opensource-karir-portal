import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jobsp.settings')
django.setup()

from course.models import Course

print("All providers:", Course.objects.values_list('provider', flat=True))
print("Distinct active providers:", Course.objects.filter(status='Active').exclude(provider__isnull=True).exclude(provider__exact='').values_list('provider', flat=True).distinct().order_by('provider'))
