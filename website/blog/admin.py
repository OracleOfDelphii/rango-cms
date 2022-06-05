from django.contrib import admin

# Register your models here.

from .models import Category, Article, Article_Category
admin.site.register ([Category, Article, Article_Category])