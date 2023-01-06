from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from system import views
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
)


urlpatterns = [
    path('', include('system.urls', namespace='system')),
    path('admin/', admin.site.urls),
    
    path(
        'accounts/login/',
        LoginView.as_view(template_name='registration/login.html'),
        name='login',
    ),
    path(
        'accounts/logout/',
        LogoutView.as_view(),
        name='logout',
    ),
    path("accounts/register", views.register_request, name="register"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)