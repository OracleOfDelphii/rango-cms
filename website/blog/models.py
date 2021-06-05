from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    def __str__(self): #important
        return self.name


class Articles_Categories(models.Model):
    article = models.ForeignKey('Article', on_delete = models.CASCADE)
    category = models.ForeignKey('Category', on_delete = models.CASCADE)



class Article(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=50, unique=True)
    categories = models.ManyToManyField('Category', through='Articles_Categories')
    content = RichTextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)


