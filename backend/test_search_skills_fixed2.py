import django
django.setup()
from django.http import QueryDict
from pjob.refine_search import refined_search

data = QueryDict('', mutable=True)
data.setlist('refine_skill', ['css'])
jobs, searched_skills, searched_locations, searched_industry, searched_edu = refined_search(data)
print("css jobs via ORM:", len(jobs))
print("Job Titles:", [j.title for j in jobs])

data2 = QueryDict('', mutable=True)
data2.setlist('refine_skill', ['CSS'])
jobs2, searched_skills, searched_locations, searched_industry, searched_edu = refined_search(data2)
print("CSS jobs via ORM:", len(jobs2))
print("Job Titles:", [j.title for j in jobs2])
