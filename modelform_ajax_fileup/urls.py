"""modelform_ajax_fileup URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, re_path
from django.conf.urls import url
from app01 import views
urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'mf/', views.modelForm),
    url(r'ulist/', views.ulist),
    url(r'edit-(\d+)',views.edit),
    url(r'ajax/$', views.ajax),
    url(r'ajax_json/$', views.ajax_json),
    url(r'^upload/$', views.upload),
    url(r'^upload_file/$', views.upload_f),
    url(r'^ulogin/$', views.ulogin),
    url(r'^get_code/$', views.check_code),# 返回验证码图片
    url(r'^kind/$', views.kind), # kindeditor编辑器
    url(r'^upload_img/$', views.upload_img),
    url(r'^file_manager/$', views.file_manager),
    url(r'^home/$', views.home),
]
