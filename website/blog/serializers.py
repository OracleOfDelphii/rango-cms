from rest_framework import serializers
from .models import Category, Article_Category, Article


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'slug']



class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['name', 'title', 'slug', 'img', 'content', 'categories']
        
