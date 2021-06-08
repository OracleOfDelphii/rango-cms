from django import forms
from .models import Article, Category
from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError
from django.db import  IntegrityError


from rest_framework import serializers
class CategoryForm(serializers.ModelSerializer):
    name = forms.CharField(widget = forms.TextInput(attrs = {'class': 'normal'}),required=True, max_length=100) 
    slug = forms.CharField(widget = forms.TextInput(attrs = {'class': 'normal'}),required=True, max_length=100)

    class Meta:
        model = Category
        fields = ('name', 'slug')
        
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from django.forms import ModelMultipleChoiceField
class PostForm(serializers.Serializer):
    title =  serializers.CharField(required=True, max_length=100, style={'base_template': 'input.html'})
    content = serializers.CharField(style={'base_template': 'textarea.html'})
    categories = serializers.MultipleChoiceField(choices = Category.objects.all(), required=False, style={'base_template': 'select_multiple.html'})
    img = serializers.ImageField(required=False, style={'base_template': 'input.html'})
    new_categories = serializers.CharField(label='new categories', required=False) #widget = forms.TextInput(attrs = {'data-role': 'tagsinput', 'class': 'special'}))
    slug = serializers.SlugField(validators=[UniqueValidator(queryset=Article.objects.all())], style={'base_template': 'input.html'})#widget = forms.TextInput(attrs = {'class': 'normal' } )))    


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

from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput

class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'placeholder': 'username', 'class': 'form-control'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder':'Password', 'class': 'form-control'}))
