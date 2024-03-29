"""bloodeal URL Configuration

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
from django.urls import path, include, re_path
from django.views.generic import RedirectView

from accounts.views import sentry_error, generate_pdf

favicon_view = RedirectView.as_view(url='/static/img/favicon.png',
                                    permanent=True)

urlpatterns = [
    re_path(r'^favicon\.ico$', favicon_view),
    path('', include("accounts.urls"), name="accounts"),
    path('profiles/', include("profiles.urls"), name="profiles"),
    path('blurays/', include("blurays.urls"), name="blurays"),
    path('deals/', include("deals.urls"), name="deals"),
    path('movies/', include("movies.urls"), name="movies"),
    path('people/', include("people.urls"), name="people"),
    path('requests/', include("user_requests.urls"), name="user_requests"),
    path('api/', include("api.urls"), name="api"),
    path('site-admin/', admin.site.urls),
    path('sentry-debug/', sentry_error, name="sentry"),
    path('pdf/', generate_pdf, name="pdf"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
