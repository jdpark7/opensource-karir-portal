from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError

class Course(models.Model):
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    instructor = models.CharField(max_length=255)
    provider = models.ForeignKey(
        'peeldb.Company',
        on_delete=models.CASCADE,
        related_name='provided_courses',
        null=True,
        blank=True,
        limit_choices_to={'company_type': 'education'},
        help_text='Select a provider company (must be an Education type)'
    )
    provider_user = models.ForeignKey('peeldb.User', on_delete=models.CASCADE, related_name="courses", null=True, blank=True)
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
        # run validation before saving
        self.full_clean()
        super(Course, self).save(*args, **kwargs)

    def clean(self):
        """
        Ensure that if a provider Company is set, its company_type is Education.
        """
        if self.provider:
            try:
                if str(self.provider.company_type) != 'education':
                    raise ValidationError({'provider': 'Selected company is not an Education provider.'})
            except AttributeError:
                raise ValidationError({'provider': 'Invalid provider selected.'})

    def __str__(self):
        return self.name
