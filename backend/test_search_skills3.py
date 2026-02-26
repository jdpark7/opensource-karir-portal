import django
django.setup()
from peeldb.models import JobPost
from django.db.models import Q
jobs = JobPost.objects.filter(status='Live').filter(skills__name__icontains='css').values_list('title', flat=True)
print("ORM Jobs with css matching:", list(jobs))
