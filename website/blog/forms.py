from django import forms
from .models import Article, Category
from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError
from django.db import  IntegrityError
from ckeditor.fields import RichTextFormField

class CategoryForm(forms.ModelForm):
    name = forms.CharField(widget = forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'name'}), required=False, max_length=100) 
    slug = forms.CharField(widget = forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'slug'}), required=False, max_length=100)

    def clean(self):
        cleaned_data = super().clean()
        name =  cleaned_data.get("name")        
        slug = cleaned_data.get("slug")
        if not (name):
            raise ValidationError("Field name is required")
        if not (slug):
            raise ValidationError("Field slug is required")



    class Meta:
        model = Category
        fields = '__all__'
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from django.forms import ModelMultipleChoiceField


class PostForm(forms.ModelForm):
    title = forms.CharField(required = True, max_length = 100, widget = forms.TextInput(attrs = {'class': 'normal', 'placeholder' : 'title'}) )
    content = RichTextField()
    categories = ModelMultipleChoiceField(queryset = Category.objects.all(), widget = forms.CheckboxSelectMultiple(attrs = {'class': 'normal list-unstyled'}), required = False)
    img = forms.ImageField(required=False, widget = forms.ClearableFileInput(attrs = {'class': 'normal', 'style': 'padding: 2em'}))
    new_categories = forms.CharField(label='new categories', required=False, widget = forms.TextInput(attrs = {'data-role': 'tagsinput', 'class': 'special', 'placeholder' : 'new category + enter'}))
    slug = forms.SlugField(widget = forms.TextInput(attrs = {'class': 'normal', 'placeholder' : 'slug' } ))
    class Meta:
        model  = Article
        fields = ('content','title','slug', 'img', 'categories', 'new_categories')
        exclude = ('author',)

    def clean_img(self):
        data = self.cleaned_data['img']
        return data


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


    def clean_categories(self):
        data = self.cleaned_data['categories']
        return data
 

    def clean_new_categories(self):
        data = self.cleaned_data['new_categories']
        return data


     
    def clean(self):
        cleaned_data = super().clean()
        new_categories = cleaned_data.get("new_categories")        
        categories = cleaned_data.get("categories")
        if not (categories or new_categories):
            raise ValidationError("either add a new category or choose from categories")

    def save(self, commit=True,  **kwargs):
        try:
            self.title = self.cleaned_data['title'] 
            self.slug = self.cleaned_data['slug']
            self.content = self.cleaned_data['content']
            self.categories = self.cleaned_data['categories']
            self.new_categories = self.cleaned_data['new_categories']
            self.img = self.cleaned_data['img']    
            article = super(PostForm, self).save(commit=False)
        # do custom stuff

            if 'author' in kwargs:
                article.author = kwargs['author']
        # change here later
            if commit:
                return article.save()
        except Exception as ex:
            print(ex)
            return None
        return article


from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from django.forms import CheckboxInput
class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(required=True, widget=TextInput(attrs={'placeholder': 'username', 'class': 'form-control'}))
    password = forms.CharField(required=True, widget=PasswordInput(attrs={'placeholder':'Password', 'class': 'form-control'}))
    remember = forms.BooleanField(required = False, label = "Remember me")
