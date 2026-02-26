import django
django.setup()
from peeldb.models import JobPost
from haystack.query import SearchQuerySet

term = 'css'
matching_job_posts = JobPost.objects.filter(
    status="Live",
    skills__name__icontains=term
)

class MockResult:
    def __init__(self, obj):
        self.object = obj
        self.pk = obj.pk
        
results = [MockResult(obj) for obj in matching_job_posts]
print("Manual list comprehension matching objs:", len(results))
from django.http import QueryDict
from pjob.refine_search import refined_search

data = QueryDict('', mutable=True)
data.setlist('refine_skill', ['css'])
jobs, searched_skills, searched_locations, searched_industry, searched_edu = refined_search(data)
print("css jobs via refined search:", len(jobs))
