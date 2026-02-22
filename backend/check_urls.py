import os
import sys
import django
from django.conf import settings
from django.urls import reverse

# Add the project directory to sys.path
sys.path.append(os.getcwd())

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jobsp.settings")
django.setup()

print("Checking URLs...")
try:
    print(f"upload_profilepic: {reverse('my:upload_profilepic')}")
except Exception as e:
    print(f"upload_profilepic error: {e}")

try:
    # Assuming language_id is a string or int, use '1' as dummy
    print(f"delete_language: {reverse('my:delete_language', args=['1'])}")
except Exception as e:
    print(f"delete_language error: {e}")

try:
    print(f"upload_resume: {reverse('my:upload_resume')}")
except Exception as e:
    print(f"upload_resume error: {e}")

try:
    print(f"delete_resume: {reverse('my:delete_resume')}")
except Exception as e:
    print(f"delete_resume error: {e}")
