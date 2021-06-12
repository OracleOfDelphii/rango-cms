from django.shortcuts import render
from django.utils.text import slugify
from .serializers import CategorySerializer, ArticleSerializer, Article_Category_Serializer
from django.contrib.auth.views import LoginView
from .forms import CustomAuthForm
from django.shortcuts import redirect
from .models import  Category, Article, Article_Category
from django.contrib.auth.models import User
from django import forms
from .forms import PostForm, CategoryForm, CustomAuthForm
from django.db import IntegrityError
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer, StaticHTMLRenderer
from django.contrib.auth import logout
from rest_framework.viewsets import ModelViewSet
import json
from rest_framework import renderers
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer])
@login_required(login_url='login')
def post_success(request):
    if request.method == "GET":
        return Response(template_name =  "post_success.html")

@login_required(login_url='login', redirect_field_name=None)
def sign_out(request):
    if request.user.is_authenticated:
        logout(request)
        form = CustomAuthForm()
        return redirect('/login')
    else:
        rd = request.GET.get('next') 
        return redirect(rd)


@login_required(login_url='login')
@api_view(['GET', 'POST', 'DELETE', 'PUT', 'PATCH'])
@renderer_classes([TemplateHTMLRenderer])
def panel(request, **kwargs):
    if request.method == 'DELETE':
        print(request.get_full_path())
        print(kwargs)
        if 'json' in request.headers.get('Content-Type'):
            js = json.loads(request.body)
            if js['object_type'] == 'article':
                article_slug = js['slug']
                try:
                    Article.objects.get(slug=article_slug).delete() 
                    return Response({"successful" : 'true'}, status = status.HTTP_200_OK, template_name='article.html')
                except Exception as e: 
                    return Response({"successful" : 'false'}, status = status.HTTP_200_OK, template_name='article.html')
            elif js['object_type'] == 'category':
                category_slug = js['slug']
                try:
                    Category.objects.get(slug=category_slug).delete() 
                    return Response({"successful" : 'true'}, status = status.HTTP_200_OK, template_name='article.html')
                except Exception as e: 
                    return Response({"successful" : 'false'}, status = status.HTTP_200_OK, template_name='article.html')
        else:
            print(request.headers.get('Content-Type'))
            print('Response content is not in JSON format.')

    if request.method == 'GET': 
        if request.get_full_path() == '/panel/new_post/':
            form = PostForm()
            return render(request, 'panel.html',  {'form': form})

        elif request.get_full_path() == '/panel/settings/':
            response_body = {}
            category_form = CategoryForm()
            response_body['category_form'] = category_form
            articles = Article.objects.all()
            response_body['articles'] = articles
            print(repr(articles))
            response_body['settings'] = 'True'
            response_body['style'] =  {"template_pack": "rest_framework/inline/"}
            print(repr(response_body))
            return Response(response_body, template_name = "panel.html")
        else:
            return Response(template_name="panel.html")

    if request.method == 'POST':
        if request.get_full_path() == '/panel/settings/':
            serializer = CategoryForm(data=request.POST)
            if serializer.is_valid():
                serializer.save()
                serializer = CategoryForm()
                success_message = "successfully added"
                resp_body = {"settings": 'True', "category_form": serializer,
                                "success_message" : '', "style": {"template_pack": "rest_framework/inline/"}}
            else:                
                resp_body = {"settings": 'True', "category_form": serializer,
                                "success_message" : '',  "style": {"template_pack": "rest_framework/inline/"}}

            return Response(resp_body, template_name = 'panel.html')

        elif request.get_full_path() == '/panel/new_post/':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit = False, author = request.user)
                print(request.POST)
                if form.is_valid() and post:
                    if 'categories' in form.cleaned_data and form.cleaned_data['categories'] != '':
                        for category in form.cleaned_data['categories']:
                            ac = Article_Category(article = post, category = category)
 
                    if 'new_categories' in form.cleaned_data and form.cleaned_data['new_categories'] != '':
                        for cat in form.cleaned_data['new_categories'].split(','):
                            try:
                                new_cat = Category(name = cat, slug = slugify(cat))
                                new_cat.save()
                                ac = Article_Category(article = post, category = new_cat)
                                ac.save()
                                form.save(commit = True)
                            except IntegrityError as e:  
                                return Response({'form': form, 'style': {}, "error" : "invalid category entry"}, template_name='panel.html')


                form.save(commit=True)
                return redirect("/panel/new_post/success", content_type='application/json')
            
            else:
                return Response({'form': form, 'style': {}}, template_name='panel.html')


class login(LoginView):
    template_name = 'login.html'
    form_class = CustomAuthForm
    remember = forms.BooleanField(required = False)

    def form_valid(self, form):

        remember_me = form.cleaned_data['remember']  # get remember me data from cleaned_data of form
        if not remember_me:
            self.request.session.set_expiry(0)  # if remember me is 
            self.request.session.modified = True
        return super(login, self).form_valid(form)
   
    class Meta:
        fields = ['username', 'password', 'remember']


@api_view(['GET'])
def delete_view(request, slug):
    return Response({"nothig": "nothing"}, template_name = 'index.html')

@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer])
def category_view(request, slug):
    category = Category.objects.get(slug = slug)
    articles = Article.objects.filter(categories__in = [category])
    return Response({'articles': articles}, template_name='category.html')

@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer])
def article_view(request, slug):
    article =  Article.objects.get(slug = slug)
    return Response({'article': article}, template_name='Article.html')

@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer])
def index(request):
    articles = Article.objects.all()
    return Response({'articles': articles}, template_name = 'index.html')
