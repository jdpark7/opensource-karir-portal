from haystack.query import SearchQuerySet
from pjob.models import Skill
print(list(SearchQuerySet().models(JobPost).filter(skills__icontains='css').values('id', 'title')))
