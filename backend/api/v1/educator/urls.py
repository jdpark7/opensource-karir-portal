"""
Educator API routing — mirrors recruiter API endpoints but scoped to educators.

This module reuses the recruiter view implementations where the behavior
is identical, allowing the front-end to call `/api/v1/educator/...` paths.
"""
from django.urls import path, include
from api.v1.recruiter import views as recruiter_views
from api.v1.recruiter import auth_views as recruiter_auth_views
from . import auth_views as educator_auth_views
from api.v1.recruiter import job_views as recruiter_job_views
from api.v1.recruiter import analytics_views as recruiter_analytics_views
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet
from . import course_views

app_name = "educator"

router = DefaultRouter()
router.register('', CourseViewSet, basename='educator')

urlpatterns = [
    # ===== AUTH =====
    path("auth/register/", recruiter_auth_views.register, name="register"),
    path("auth/login/", educator_auth_views.login, name="login"),
    path("auth/logout/", recruiter_auth_views.logout, name="logout"),

    path("auth/verify-email/", recruiter_auth_views.verify_email, name="verify-email"),
    path("auth/resend-verification/", recruiter_auth_views.resend_verification, name="resend-verification"),

    path("auth/forgot-password/", recruiter_auth_views.forgot_password, name="forgot-password"),
    path("auth/reset-password/", recruiter_auth_views.reset_password, name="reset-password"),
    path("auth/change-password/", recruiter_auth_views.change_password, name="change-password"),

    path("auth/accept-invitation/", recruiter_auth_views.accept_invitation, name="accept-invitation"),
    path("auth/me/", recruiter_auth_views.me, name="me"),

    path("profile/update/", recruiter_auth_views.update_profile, name="profile-update"),
    path("profile/picture/", recruiter_auth_views.upload_profile_picture, name="profile-picture"),

    path("auth/google/url/", recruiter_auth_views.google_auth_url, name="google-auth-url"),
    path("auth/google/callback/", recruiter_auth_views.google_callback, name="google-callback"),
    path("auth/google/complete/", recruiter_auth_views.google_complete, name="google-complete"),

    # ===== TEAM (reuse recruiter handlers for now) =====
    path("team/", recruiter_views.list_team_members, name="team-list"),
    path("team/<int:user_id>/", recruiter_views.get_team_member, name="team-detail"),
    path("team/<int:user_id>/update/", recruiter_views.update_team_member, name="team-update"),
    path("team/<int:user_id>/remove/", recruiter_views.remove_team_member, name="team-remove"),

    path("team/invite/", recruiter_views.invite_team_member, name="team-invite"),
    path("team/invitations/", recruiter_views.list_invitations, name="invitations-list"),
    path("team/invitations/<int:invitation_id>/resend/", recruiter_views.resend_invitation, name="invitation-resend"),
    path("team/invitations/<int:invitation_id>/cancel/", recruiter_views.cancel_invitation, name="invitation-cancel"),

    # ===== JOBS & DASHBOARD =====
    path("dashboard/stats/", recruiter_job_views.get_dashboard_stats, name="dashboard-stats"),

    path("analytics/applications/", recruiter_analytics_views.get_application_analytics, name="application-analytics"),
    path("jobs/<int:job_id>/analytics/", recruiter_analytics_views.get_job_application_analytics, name="job-analytics"),

    path("jobs/metadata/", recruiter_job_views.get_job_form_metadata, name="jobs-metadata"),

    path("jobs/", recruiter_job_views.list_jobs, name="jobs-list"),
    path("jobs/create/", recruiter_job_views.create_job, name="jobs-create"),
    path("jobs/<int:job_id>/", recruiter_job_views.get_job, name="jobs-detail"),
    path("jobs/<int:job_id>/update/", recruiter_job_views.update_job, name="jobs-update"),
    path("jobs/<int:job_id>/delete/", recruiter_job_views.delete_job, name="jobs-delete"),

    path("jobs/<int:job_id>/publish/", recruiter_job_views.publish_job, name="jobs-publish"),
    path("jobs/<int:job_id>/close/", recruiter_job_views.close_job, name="jobs-close"),

    path("jobs/<int:job_id>/applicants/", recruiter_job_views.get_job_applicants, name="jobs-applicants"),
    path("jobs/<int:job_id>/applicants/<int:applicant_id>/", recruiter_job_views.get_applicant_detail, name="applicant-detail"),
    path("jobs/<int:job_id>/applicants/<int:applicant_id>/update/", recruiter_job_views.update_applicant_status, name="applicant-update"),

    # ===== COMPANY =====
    path("company/profile/", recruiter_views.get_company_profile, name="company-profile"),
    path("company/profile/update/", recruiter_views.update_company_profile, name="company-profile-update"),

    # Course-specific endpoints
    path("courses/metadata/", course_views.get_course_form_metadata, name="courses-metadata"),
    path("courses/dashboard/stats/", course_views.get_dashboard_stats, name="courses-dashboard-stats"),
    path("courses/", course_views.list_courses, name="courses-list"),
    path("courses/create/", course_views.create_course, name="courses-create"),
    path("courses/<int:course_id>/", course_views.get_course, name="courses-detail"),
    path("courses/<int:course_id>/update/", course_views.update_course, name="courses-update"),
    path("courses/<int:course_id>/delete/", course_views.delete_course, name="courses-delete"),
    path("courses/<int:course_id>/status/", course_views.set_course_status, name="courses-status"),
    path("courses/bulk/", course_views.bulk_course_action, name="courses-bulk"),

    # Course resource router (educator-specific)
    path('', include(router.urls)),
]
