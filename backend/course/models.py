from django.db import models
from django.utils.text import slugify

class Course(models.Model):
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    instructor = models.CharField(max_length=255)
    provider = models.CharField(max_length=255)
    url = models.URLField()
    course_img = models.ImageField(upload_to='course_images/', null=True, blank=True)
    description = models.TextField()
    keywords = models.CharField(max_length=255, help_text="Comma separated keywords (max 4)")
    skills = models.TextField(blank=True, null=True, help_text="Skills acquired after this course")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Course, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
