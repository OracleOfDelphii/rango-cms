import imp
from pipes import Template
from django import forms
from .models import Article, Category
from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError
from django.db import  IntegrityError
from ckeditor.fields import RichTextFormField
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker

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

from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    author = forms.ModelChoiceField(queryset=User.objects.all(), required=True)
    title = forms.CharField(required = True, max_length = 100, widget = forms.TextInput(attrs = {'class': 'normal form-control', 'placeholder' : 'title'}) )
    content = RichTextField()
    categories = ModelMultipleChoiceField(queryset = Category.objects.all(), widget = forms.CheckboxSelectMultiple(attrs = {'class': 'normal list-unstyled'}), required = False)
    img = forms.ImageField(required=False, widget = forms.ClearableFileInput(attrs = {'class': 'normal', 'style': 'padding: 2em'}))
    new_categories = forms.CharField(label='new categories', required=False, widget = forms.TextInput(attrs = {'data-role': 'tagsinput', 'class': 'form-control special', 'placeholder' : 'new category + enter'}))
    slug = forms.SlugField(widget = forms.TextInput(attrs = {'class': 'normal form-control', 'placeholder' : 'slug' } ))
    date = forms.DateTimeField(widget=DateTimePicker(
        options={
                'useCurrent': True,
                'collapse': True,
            },
            attrs={
                'append': 'fa fa-calendar',
                'icon_toggle': True,
            }
        ),
        input_formats=['%m/%d/%Y %I:%M %p']
    )

    class Meta:
        model  = Article
        fields = ('author','content','title','slug', 'img', 'categories', 'new_categories', 'is_published', 'date')
   

    def clean_img(self):
        data = self.cleaned_data['img']
        return data

    def clean_date(self):
        data = self.cleaned_data['date']
        return data

    def clean_is_published(self):
        data = self.cleaned_data['is_published']
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
        data = self.cleaned_data['slug'].lower()
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
        return cleaned_data