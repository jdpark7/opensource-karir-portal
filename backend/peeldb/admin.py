from django.contrib import admin
from django import forms
from peeldb.models import (
    User,
    Google,
    Company,
    Country,
    State,
    City,
    Skill,
    Industry,
    UserEmail,
    Language,
    Qualification,
    FunctionalArea,
    simplecontact,
    JobPost,
)


class LocationAdminMixin:
    """
    Mixin for location models (Country, State, City) to restrict permissions.
    Added as part of location cleanup initiative (LOCATION_CLEANUP_PLAN.md Phase 1)

    Only superusers can add/edit/delete locations to maintain data quality.
    """

    def has_add_permission(self, request):
        """Only superusers can create locations"""
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        """Only superusers can edit locations"""
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        """Only superusers can delete locations"""
        return request.user.is_superuser


@admin.register(Country)
class CountryAdmin(LocationAdminMixin, admin.ModelAdmin):
    """Admin interface for Country model"""
    list_display = ('id', 'name', 'slug', 'status')
    list_filter = ('status',)
    search_fields = ('name', 'slug')
    ordering = ('name',)


@admin.register(State)
class StateAdmin(LocationAdminMixin, admin.ModelAdmin):
    """Admin interface for State model"""
    list_display = ('id', 'name', 'country', 'slug', 'status')
    list_filter = ('country', 'status')
    search_fields = ('name', 'slug')
    ordering = ('country__name', 'name')
    raw_id_fields = ('country',)


@admin.register(City)
class CityAdmin(LocationAdminMixin, admin.ModelAdmin):
    """Admin interface for City model"""
    list_display = ('id', 'name', 'state', 'get_country', 'status', 'job_count')
    list_filter = ('status', 'state__country', 'state')
    search_fields = ('name', 'slug')
    ordering = ('state__name', 'name')
    raw_id_fields = ('state',)
    readonly_fields = ('job_count',)

    def get_country(self, obj):
        """Display country name"""
        return obj.state.country.name if obj.state and obj.state.country else '-'
    get_country.short_description = 'Country'
    get_country.admin_order_field = 'state__country__name'

    def job_count(self, obj):
        """Display number of jobs using this city"""
        from peeldb.models import JobPost
        count = JobPost.objects.filter(location=obj).count()
        return count
    job_count.short_description = 'Jobs'

    def get_queryset(self, request):
        """Optimize queryset with prefetch"""
        qs = super().get_queryset(request)
        return qs.select_related('state', 'state__country')


admin.site.register(Skill)
admin.site.register(Language)
admin.site.register(FunctionalArea)
class CompanyAdminForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Required fields: name, address, size, company_type, phone_number, email, slug
        required = {'name', 'address', 'size', 'company_type', 'phone_number', 'email', 'slug'}
        for fname, field in self.fields.items():
            field.required = fname in required


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    form = CompanyAdminForm
    list_display = ('id', 'name', 'slug', 'is_active', 'company_type')
    search_fields = ('name', 'slug', 'website', 'email')
    list_filter = ('is_active', 'company_type')
    ordering = ('name',)
@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'slug')
    search_fields = ('name',)

class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make all fields optional except the essential ones
        required_fields = ['email', 'username', 'password', 'user_type']
        for field_name, field in self.fields.items():
            if field_name not in required_fields:
                field.required = False

    def save(self, commit=True):
        user = super().save(commit=False)
        # Hash password if entered in plain text
        if user.password and not user.password.startswith('pbkdf2_'):
            user.set_password(user.password)
        if commit:
            user.save()
            self.save_m2m()
        return user

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm
    list_display = ('email', 'username', 'user_type', 'is_active', 'is_staff')
    search_fields = ('email', 'username')
    list_filter = ('user_type', 'is_active', 'is_staff')
admin.site.register(Google)
admin.site.register(UserEmail)
admin.site.register(Qualification)


@admin.register(simplecontact)
class ContactInquiryAdmin(admin.ModelAdmin):
    """Admin interface for contact inquiries"""
    list_display = ('first_name', 'last_name', 'email', 'enquery_type', 'subject', 'contacted_on')
    list_filter = ('enquery_type', 'contacted_on')
    search_fields = ('first_name', 'last_name', 'email', 'subject', 'comment')
    readonly_fields = ('contacted_on',)
    date_hierarchy = 'contacted_on'
    ordering = ('-contacted_on',)

    fieldsets = (
        ('Contact Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Inquiry Details', {
            'fields': ('enquery_type', 'subject', 'comment')
        }),
        ('Metadata', {
            'fields': ('contacted_on',)
        }),
    )

class JobPostAdminForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Required fields: Title, Location, Job Type, Work Mode, Company Name, Company Address, Company Links, Skills, Qualification, User
        required = {'user', 'title', 'location', 'job_type', 'work_mode', 'company_name', 'company_address', 'company_links', 'skills', 'edu_qualification'}
        for fname, field in self.fields.items():
            if fname not in required:
                field.required = False

@admin.register(JobPost)
class JobPostAdmin(admin.ModelAdmin):
    form = JobPostAdminForm
    list_display = ('title', 'user', 'company', 'status', 'job_type', 'created_on')
    search_fields = ('title', 'user__email', 'company__name', 'code')
    list_filter = ('status', 'job_type', 'work_mode', 'fresher')
    filter_horizontal = ('location', 'industry', 'job_interview_location', 'keywords', 'edu_qualification', 'agency_recruiters', 'skills')
    prepopulated_fields = {'slug': ('title',)}
    
    fieldsets = (
        ('Required Job Details', {
            'fields': (
                'user',
                'title',
                'location',
                'job_type',
                'work_mode',
                'company_name',
                'company_address',
                'company_links',
                'skills',
                'edu_qualification',
            )
        }),
        ('Optional Basics', {
            'classes': ('collapse',),
            'fields': (
                'slug', 'company', 'status', 'vacancies', 'job_role',
                'code', 'description', 
            )
        }),
        ('Salary & Experience', {
            'classes': ('collapse',),
            'fields': (
                'fresher', 'min_year', 'max_year', 'min_month', 'max_month',
                'salary_type', 'min_salary', 'max_salary', 'show_salary',
                'seniority_level'
            )
        }),
        ('Company Info', {
            'classes': ('collapse',),
            'fields': (
                'company_description', 'company_emails',
            )
        }),
        ('Applications & Settings', {
            'classes': ('collapse',),
            'fields': (
                'application_method', 'application_url', 
                'hiring_timeline', 'hiring_priority', 'relocation_required',
                'travel_percentage', 'benefits', 'language_requirements',
                'required_certifications', 'preferred_certifications',
            )
        }),
        ('Taxonomy', {
            'classes': ('collapse',),
            'fields': (
                'industry', 'keywords', 'major_skill',
            )
        }),
        ('Location specifics', {
            'classes': ('collapse',),
            'fields': (
                'country', 'pincode', 'job_interview_location',
            )
        }),
        ('Dates & Metadata', {
            'classes': ('collapse',),
            'fields': (
                'created_on', 'published_on', 'closed_date', 
                'meta_title', 'meta_description',
            )
        }),
        ('Government Jobs', {
            'classes': ('collapse',),
            'fields': (
                'govt_job_type', 'application_fee', 'selection_process', 
                'how_to_apply', 'important_dates', 'govt_from_date', 
                'govt_to_date', 'govt_exam_date', 'age_relaxation',
            )
        }),
        ('Walk-in Settings', {
            'classes': ('collapse',),
            'fields': (
                'walkin_contactinfo', 'walkin_show_contact_info', 
                'walkin_from_date', 'walkin_to_date', 'walkin_time',
            )
        }),
        ('Agency Tools', {
            'classes': ('collapse',),
            'fields': (
                'agency_job_type', 'agency_invoice_type', 'agency_amount', 
                'agency_client', 'agency_category', 'agency_recruiters',
            )
        }),
        ('Visa Information', {
            'classes': ('collapse',),
            'fields': (
                'visa_required', 'visa_country', 'visa_type',
            )
        }),
    )
    readonly_fields = ('created_on',)

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'user', None) is None:
            obj.user = request.user
        super().save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "country":
            indonesia = Country.objects.filter(name__icontains="Indonesia").first()
            if indonesia:
                kwargs["initial"] = indonesia.id
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

