"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
import xadmin
from django.contrib import admin
from rest_framework.documentation import include_docs_urls
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from article.views import IndexView,UserProfileView,UserProfileEditView

urlpatterns = [
    path('admin/',admin.site.urls),
    path('xadmin/', xadmin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('doc/',include_docs_urls(title="Huu Api")),
    path('accounts/', include('allauth.urls')),
    path('api/', include('api.urls')),

    path('',IndexView.as_view(),name='index'),
    path('article/',include('article.urls')),
    path('accounts/profile/<int:user_id>/', UserProfileView.as_view(), name='profile'),
    path('accounts/profile/edit/', UserProfileEditView.as_view(), name='profile_edit'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

