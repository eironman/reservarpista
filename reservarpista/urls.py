"""reservarpista URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    url(r'^authentication/', include('authentication.urls', 'authentication')),
    url(r'^management/', include('management.urls', 'management')),
    url(r'^signup/', include('signup.urls', 'signup')),
    url(r'^admin/', admin.site.urls),
    url(r'^', include('core.urls', 'core')),
    url(r'^(?P<sport_slug>[a-z0-9\-]+)/(?P<location_slug>[a-z\-]+)/', include('search.urls', 'search')),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)