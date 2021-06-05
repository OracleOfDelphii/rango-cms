from django import forms
from .models import Article, Category
from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError

class CategoryForm(forms.ModelForm):
    name = forms.CharField(widget = forms.TextInput(attrs = {'class': 'normal'}),required=True, max_length=100) 
    slug = forms.CharField(widget = forms.TextInput(attrs = {'class': 'normal'}),required=True, max_length=100)

    class Meta:
        model = Category
        fields = ('name', 'slug')
        
from django.forms import ModelMultipleChoiceField

class PostForm(forms.ModelForm):
    title = forms.CharField(widget = forms.TextInput(attrs = {'class': 'normal'}),required=True, max_length=100)
    content = RichTextField()
    categories = ModelMultipleChoiceField(queryset = Category.objects.all(), widget = forms.CheckboxSelectMultiple, required=False)
    new_categories = forms.CharField(label='new categories', required=False, widget = forms.TextInput(attrs = {'data-role': 'tagsinput', 'class': 'special'}))
    slug = forms.SlugField(widget = forms.TextInput(attrs = {'class': 'normal' } ))
    class Meta:
        model  = Article
        fields = ('content','title','slug', 'categories', 'new_categories')
        exclude = ('author',)
    
    def clean_title(self):
        data = self.cleaned_data['title']
        if data == None:
            raise ValidationError("Field title is required")
        return data

    def clean_content(self):
        data = self.cleaned_data['content']
        if data == None:
            raise ValidationError("Field content is required")
        return data

    def clean_slug(self):
        data = self.cleaned_data['slug']
        if data == None:
            raise ValidationError("Field slug is required")
        return data
     
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
