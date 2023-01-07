from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from system import views
from rest_framework import routers, serializers, viewsets
from django.contrib.auth.views import LogoutView
from system.views import MyLoginView

router = routers.DefaultRouter()
router.register(r'scores', views.ScoreViewSet)



urlpatterns = [
    path('', include('system.urls', namespace='system')),
    path('api/', include((router.urls, 'app_name'), namespace='instance_name')),
    path('admin/', admin.site.urls),
    
    path('accounts/login/',
        MyLoginView.as_view(),
        name='login',
    ),
    path(
        'accounts/logout/',
        LogoutView.as_view(),
        name='logout',
    ),
    path("accounts/register", views.register_request, name="register"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)