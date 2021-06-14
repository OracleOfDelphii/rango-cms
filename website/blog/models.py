from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.utils import timezone
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    def __str__(self): #important
        return self.name


class Article_Category(models.Model):
    article = models.ForeignKey('Article', on_delete = models.CASCADE)
    category = models.ForeignKey('Category', on_delete = models.CASCADE)


class Article(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    img = models.ImageField(upload_to='articles', default = 'articles/default.jpg')
    categories = models.ManyToManyField('Category', through='Article_Category')
    content = RichTextField() # unique = True :))
    date = models.DateTimeField(default = timezone.now, blank=False)
    is_published = models.BooleanField(default = True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


