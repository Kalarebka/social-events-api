"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("users/", include("users.urls")),
    path("admin/", admin.site.urls),
    path("events/", include("events.urls")),
    path("messagebox/", include("messagebox.urls")),
    path("auth/", include("rest_framework.urls")),  # login/logout for browsable API
    path("rest-auth/", include("dj_rest_auth.urls")),
    path("register/", include("dj_rest_auth.registration.urls")),
    path(
        "schema/", SpectacularAPIView.as_view(), name="schema"
    ),  # auto schema generation
    path("schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
