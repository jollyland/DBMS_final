"""testfile URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include, re_path
from django.conf.urls import url
from main import views

from main.models import Academy

urlpatterns = [
    path('admin/', admin.site.urls),
    path('search_uni/', views.search_uni),
    path('uni_search_result/', views.uni_result),
    path('dpt_search_result/', views.dpt_result),

    path('search_apt/', views.search_apt),
    path('search_gp/', views.search_gp),
    path('list_all/', views.list_all),
    path('uni/<str:uniid>', views.uni_each),
    path('dprt/<str:dprtid>', views.dprt_each),
    path('gp/<str:name>',views.gp_each),
    re_path(r'^.*', views.main),
]