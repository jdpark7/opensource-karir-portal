from peeldb.models import User, Company
from django.utils.text import slugify

# 1. Create Company
company_name = "InaWorks Demo Company"
company_slug = slugify(company_name)

company, created = Company.objects.get_or_create(
    slug=company_slug,
    defaults={
        "name": company_name,
        "address": "Seoul, South Korea",
        "phone_number": "010-1234-5678",
        "profile": "This is a demo company created for testing purposes.",
        "email": "contact@inaworks-demo.com",
        "company_type": "Company",
        "is_active": True
    }
)

if created:
    print(f"[SUCCESS] Created Company: {company.name}")
else:
    print(f"[INFO] Using existing Company: {company.name}")

# 2. Create Recruiter User
email = "recruiter@inaworks.com"
username = "recruiter"
password = "password123"

try:
    user = User.objects.get(email=email)
    print(f"[INFO] User {email} already exists. Updating password...")
    user.set_password(password)
    user.company = company
    user.user_type = "EM"
    user.is_active = True
    user.email_verified = True
    user.save()
    print(f"[SUCCESS] Updated User: {email} with password '{password}'")
except User.DoesNotExist:
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )
    user.user_type = "EM"
    user.company = company
    user.is_active = True
    user.email_verified = True
    user.save()
    print(f"[SUCCESS] Created User: {email}")
    print(f"Username: {username}")
    print(f"Password: {password}")

print("\nYou can now login at http://localhost:5173/ with:")
print(f"Email: {email}")
print(f"Password: {password}")
