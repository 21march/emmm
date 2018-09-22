"""supermarket URL Configuration

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
from django.conf.urls import url
from django.contrib import admin

from login.views import RegisterView, LoginView, index, CenterView, InforView, AddressView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$',LoginView.as_view(),name='login'),
    url(r'^index/$',index,name='index'),
    url(r'^reg/$',RegisterView.as_view(),name='register'),
    url(r'^center/$',CenterView.as_view(),name='center'),
    url(r'^infor/$',InforView.as_view(),name='infor'),
    # url(r'^address/$',AddressView.as_view(),name='address'),
]
