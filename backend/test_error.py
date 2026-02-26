import django
django.setup()
from django.test import RequestFactory
from django.urls import reverse
from pjob.views import job_skills

factory = RequestFactory()
request = factory.get('/css-jobs/')
request.META['REMOTE_ADDR'] = '127.0.0.1'

try:
    response = job_skills(request, skill='css')
    print("job_skills CSS status code:", response.status_code)
except Exception as e:
    import traceback
    traceback.print_exc()
