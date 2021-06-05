"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

from .forms import CustomAuthForm
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path(r'', views.index, name='home'),
    path(r'category/<slug:slug>', views.category_view, name='category'),
    path(r'panel/new_post', views.panel, name='new_post'),
    path(r'panel/settings', views.panel, name='settings'),
    path(r'panel/new_post/success', views.post_success, name='post_success'),
	path(r'panel', views.panel, name='panel'),
    path(r'article/<slug:slug>', views.article_view, name='article'),
	path(r'sign_out', views.sign_out, name='sign_out'),
	path('login/', views.login.as_view(template_name='login.html'), name='login', kwargs={"authentication_form":CustomAuthForm}),

	path(r'delete/', views.panel, name='delete'),
]
