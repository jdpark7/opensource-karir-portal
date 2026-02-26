import django
django.setup()
from django.test import RequestFactory
from django.urls import reverse
from pjob.views import job_skills, skill_fresher_jobs

factory = RequestFactory()
request = factory.get('/')
request.META['REMOTE_ADDR'] = '127.0.0.1'

response = job_skills(request, skill='css')
print("job_skills CSS status code:", response.status_code)

response2 = skill_fresher_jobs(request, skill_name='css')
print("skill_fresher_jobs CSS status code:", response2.status_code)
