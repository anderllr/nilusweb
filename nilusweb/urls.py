"""nilusweb URL Configuration

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
from django.conf.urls import url,include
from django.contrib import admin
from django.contrib.auth.views import login
from core import views
from django.contrib.auth.views import logout
from django.conf.urls.static import  static
from django.conf import settings

urlpatterns = [
    url(r'^$',login,{'template_name' : 'signin.html'}, name='signin'),
    url(r'^conta/', include('accounts.urls')),
    url(r'^principal/', include('principal.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^sair/$', logout, {'next_page': 'signin'}, name='logout'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
