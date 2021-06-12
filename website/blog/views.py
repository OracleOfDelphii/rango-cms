from django.shortcuts import render
from django.utils.text import slugify
from .serializers import CategorySerializer, ArticleSerializer, Article_Category_Serializer
# Create your views here.

from django.shortcuts import get_object_or_404, HttpResponseRedirect, get_list_or_404, redirect
from .models import  Category, Article, Article_Category
from django.contrib.auth.models import User
from django import forms
from .forms import PostForm, CategoryForm
from django.db import IntegrityError
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.forms.models import model_to_dict
from rest_framework.decorators import api_view
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
from .forms import CustomAuthForm

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

from website.settings import MEDIA_URL

from django.core.files.base import ContentFile


from rest_framework import status


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
                    post.save()
                    print("cdata:", form.cleaned_data['categories'])
                    if 'categories' in form.cleaned_data and form.cleaned_data['categories'] != '':
                        for i in form.cleaned_data['categories']:
                            print("cat", i)

                            ac = Article_Category(article = post, category = i)
                            ac.save() 

                    print("cdata:", form.cleaned_data['new_categories'])
                    if 'new_categories' in form.cleaned_data and form.cleaned_data['new_categories'] != '':
                        for cat in form.cleaned_data['new_categories'].split(','):
                            new_cat = Category(name = cat, slug = slugify(cat))
                            print("new_cat", new_cat)
                            new_cat.save()
                            ac = Article_Category(article = post, category = new_cat)
                            ac.save()
                            try:
                                form.save(commit = True)

                            except IntegrityError as e:
                                err = f"Category: {cat} exists."
                                # only for test now, will use django-rest later
                                print(err)              
                                return Response({'form': form, 'style': {}}, template_name='panel.html')
                
                form.save(commit=True)      
                return redirect("/panel/new_post/success", content_type='application/json')
        # only for test now, will use django-rest later
            else:
                print(form.data)

                return Response({'form': {}, 'style': {}}, template_name='panel.html')


# problem, need to break Panel into smaller pieces
# problem, need to write serializer for every view including PANEL
class Panel(ModelViewSet):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'panel.html'
    queryset = Article.objects.all()
    #serializer_class = ArticleSerializer


    def get(self, request): 
        form = PostForm()
        return Response({'form': form}, template_name='panel.html')
    
    
    def put(self, request):
        pass

    def delete(self, request):  
        if True:
            print(repr(request))
            if 'json' in request.headers.get('Content-Type'):
                js = json.loads(request.body)
                article_slug = js['slug']
                print(article_slug)
                try:
                    Article.objects.get(slug=article_slug).delete()
                    return Response({'delete': 'success'})
                except Exception as e:
                    return Response({'delete': 'fail'})
            else:
                print('Response content is not in JSON format.') 
        else:
            print(request.get_full_path())
            return Response({'delete': 'fail'})


    def post(self, request):
        if request.get_full_path() == '/panel/settings':
            serializer = CategoryForm(request.POST)
            if serializer.is_valid():
                serializer.save()
                serializer = CategoryForm()
                success_message = "successfully added"
                resp_body = {"settings": True, "serializer": serializer,
                                "success_message" : success_message}
            else:                
                resp_body = {"settings": True, "serializer": serializer,
                                "success_message" : success_message}

            return Response(resp_body)

        elif request.get_full_path() == '/panel/new_post/':
            if request.POST:
                form = PostForm(request.data)
                print(form.cleaned_data, form.data)
                if form.is_valid():
                    post = form
                    form.save(author = request.user)
                    try:
                        print(form.cleaned_data)
                        post.save()
                        #form.save_m2m() override create for PostForm to support many to many relationship
                    except Exception as e:
                        print(e)
                        # only for test now, will use django-rest later
                        return Response({'form': form})

                    if form.cleaned_data['new_categories'] != '':
                        for cat in form.cleaned_data['new_categories'].split(','):
                            new_cat = Category(name=cat, slug = slugify(cat))
                            new_cat.save()
                            try:
                                post.save()
                                article_category = Article_Category_Serializer(category_id = new_cat.id,
                                
                                article_id = post.id) # write serializer for Article_Category
                                article_category.save()

                            except IntegrityError as e:
                                err = f"Category: {cat} exists."
                                # only for test now, will use django-rest later
                                return render(request, 'panel.html', {'form': form})
                    return redirect("/panel/new_post/success")

            # only for test now, will use django-rest later
            else:
                form = PostForm()
                return Response({'form': form})


from django.contrib.auth.views import LoginView

from .forms import CustomAuthForm

class login(LoginView):
    template_name = 'login.html'
    form_class = CustomAuthForm

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
