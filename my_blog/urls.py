from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from two_factor.urls import urlpatterns as tf_urls


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path("",include("blogs.api.urls")),
    path('third-party/', include(tf_urls)),
    path("account/",include("user_app.api.urls")),
    path("sub/",include("sub_plan_app.api.urls")),
    path("socal/",include("socal_auth.urls")),
    path('swagger.yaml/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('auth/', include('drf_social_oauth2.urls', namespace='drf')),
    path('accounts/', include('allauth.urls')),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
