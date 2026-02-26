import django
django.setup()
from haystack.query import SearchQuerySet
from peeldb.models import JobPost
print("Jobs where skills match exact 'CSS':", list(SearchQuerySet().models(JobPost).filter(skills__in=['CSS']).values_list('title', flat=True)))
print("Jobs where skills match inexact 'css':", list(SearchQuerySet().models(JobPost).filter(skills__in=['css']).values_list('title', flat=True)))
