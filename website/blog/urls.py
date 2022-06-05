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
from django.urls import path, include
 
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path(r'panel/', views.Panel.as_view(), name='panel_home'),
    path(r'panel/new_post/', views.NewPostView.as_view(), name='new_post'),
    path(r'success/', views.SuccessView.as_view(), name='success'),
    path(r'panel/edit_post/<slug:slug>/', views.EditPostView.as_view(), name='edit_post'),
    path(r'panel/delete_post/<slug:slug>/', views.DeletePostView.as_view(), name='delete_post'),
    path(r'panel/posts/', views.ListArticles.as_view(), name='posts'),
    path(r'panel/categories/', views.ListCategories.as_view(), name='categories'),
    path(r'', views.IndexView.as_view(), name='home'),
    path(r'articles/', views.ViewArticles.as_view(), name='articles'),
    
    path(r'article/<slug:article_slug>/', views.ViewArticle.as_view(), name='article'),
    path(r'category/<slug:category_slug>/', views.ViewArticles.as_view(), name='articles_by_category'),
    
     path('login/', views.Login.as_view(), name='login'),  

]
"""
    path(r'category/<slug:slug>', views.category_view, name='category'),
    path(r'article/<slug:slug>', views.article_view, name='article'),
	path(r'sign_out/', views.sign_out, name='sign_out'),
	path(r'panel/', views.panel, name='panel'),
    path(r'panel/new_post/', views.panel, name='panel_new_post'), 
    path(r'panel/new_post/success/', views.post_success, name='post_success'),
    path('login/', views.login.as_view(template_name='login.html'), name='login'), #kwargs={"authentication_form":CustomAuthForm}),
    path(r'panel/settings/', views.panel, name = 'panel_settings'),
    path(r'panel/posts/<slug:slug>/', views.panel, name = 'panel_post'),
"""