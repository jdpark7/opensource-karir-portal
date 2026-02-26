import django
django.setup()
from haystack.query import SearchQuerySet
from peeldb.models import JobPost
print("All jobs:", SearchQuerySet().models(JobPost).count())
print("Jobs containing css:", list(JobPost.objects.filter(skills__name__icontains='css').values_list('title', flat=True)))
