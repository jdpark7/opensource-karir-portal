from django.urls import path
from api.v1.auth import views as auth_views

app_name = "educator_auth"

urlpatterns = [
    # Expose the shared auth endpoints under /api/v1/educator/auth/
    path('me/', auth_views.current_user, name='current-user'),
    path('token/refresh/', auth_views.CookieTokenRefreshView.as_view(), name='token-refresh'),
    path('logout/', auth_views.logout, name='logout'),
]
