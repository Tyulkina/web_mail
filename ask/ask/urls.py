"""ask URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import re_path
from qa.views import test,new,popular,get_question,add_question,login,signup

urlpatterns = [
    re_path(r'^$', new),
    re_path(r'^login/$',login),
    re_path(r'^signup/$',signup),
    re_path(r'^question/(?P<num>[\d]+)/$',get_question),
    re_path(r'^popular/$',popular),
    re_path(r'^new/$',new),
    re_path(r'^ask/$',add_question),
]


