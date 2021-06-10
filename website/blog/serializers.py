from rest_framework import serializers

from .models import  Category, Article, Article_Category


class CategorySerializer(serializers.ModelSerializer):
    articles = serializers.PrimaryKeyRelatedField(queryset=Article.objects.all(), many=True)
    class Meta:
        model = Category
        fields = ['name', 'slug']
        read_only_fields = ['id']



class ArticleSerializer(serializers.ModelSerializer):
    
    categories = CategorySerializer(read_only = True, many=True)
    class Meta:
        model = Article 
        fields = ['title', 'slug', 'img', 'content', 'categories'] 
        read_only_fields = ['id']

class Article_Category_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Article_Category
        fields = ['article', 'category']
