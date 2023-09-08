"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    # path('google-auth', views.google_auth, name='google_auth'),
    path('google-callback', views.google_callback, name='google_callback'),
    # path('download-manga', views.download_manga, name='download_manga'),
    path('api/v1/download-manga', views.download_manga, name='download_manga'),
    path('api/v1/download-manga-one', views.download_manga_one, name='download_manga_one'),
    path('api/v1/manga-updated', views.manga_updated, name='manga_updated'),
    path('api/v1/auth-google-drive', views.auth_google_drive, name='auth_google_drive'),
    path('api/v1/fetch-manga-updated', views.fetch_manga_updated, name='fetch_manga_updated'),
    path('api/v1/health', views.health, name='health'),
]
