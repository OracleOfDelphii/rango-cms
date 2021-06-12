from rest_framework import serializers

from .models import  Category, Article, Article_Category
from rest_framework.validators import UniqueTogetherValidator

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'slug']


class ArticleSerializer(serializers.ModelSerializer):    
    categories = CategorySerializer(read_only = True, many=True)
    class Meta:
        model = Article 
        fields = ['title', 'slug', 'img', 'content', 'categories'] 


class Article_Category_Serializer(serializers.ModelSerializer):
    queryset = Article_Category.objects.all()
    class Meta:
        model = Article_Category
        fields = ['article', 'category']


"""
class PostSerializer(serializers.Serializer):
    title =  serializers.CharField(required=True, max_length=100, style={'base_template': 'input.html', 'class': 'normal'})
    content = RichTextFormField()#style={'base_template': 'textarea.html'})
    categories = serializers.MultipleChoiceField(choices = Category.objects.all(), required=False, style={'base_template': 'select_multiple.html', 'class' : 'normal'})
    img = serializers.ImageField(required=False, style={'base_template': 'input.html', 'class': 'normal'})
    new_categories = serializers.CharField(label='new categories', required=False, style =  {'base_template': 'input.html', 'data-role': 'tagsinput', 'class': 'special'})
    slug = serializers.SlugField(validators=[UniqueValidator(queryset=Article.objects.all())], style={'base_template': 'input.html', 'class': 'normal'} )
    def save(self):
        title = self.validated_data['title']
        content = self.validated_data['content']
        categories = self.validated_data['categories']
        img = self.validated_data['img']    
        new_categories = self.validated_data['new_categories']
        slug = self.validated_data['slug']
        author = self.validated_data['author']
        article = Article(self.validated_data)
        article.save()
        
        for c in categories:
            article_category = Article_Category(article, c)
            article_category.save()

    def create(self, validated_data):
        x = self.validated_data       
        article = Article(title = x['title'], content = x['content'], img = x['img'],  slug = x['slug'], categories = x['categories'])
        return article    


    def clean(self):
        cleaned_data = super().clean()
        new_categories = cleaned_data.get("new_categories")
        categories = cleaned_data.get("categories")
        if not (categories or new_categories):
            raise ValidationError("either add a new category or choose from categories")

"""
