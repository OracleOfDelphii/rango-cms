from django.shortcuts import render

from .serializers import CategorySerializer
# Create your views here.

from django.shortcuts import get_object_or_404, HttpResponseRedirect, get_list_or_404, redirect
from .models import  Category, Article
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

@login_required(login_url='login')
def post_success(request):
    return render(request, "post_success.html")

class post_success(APIView):
    render_classes = [StaticHTMLRenderer]
    template_name = 'post_success.html'



from django.contrib.auth import logout

@login_required(login_url='login')
def sign_out(request):
    if request.user.is_authenticated:
        logout(request)
        return render(request, "logged_out.html")
    else:
        return HttpResponseRedirect('login', content_type='application/json')

from .models import Article_Category

from website.settings import MEDIA_URL

from django.core.files.base import ContentFile

def handle_uploaded_image(form, request):
    img = request.FILES['img']
    
    f = img.file

    data = f.read()
    form.cleaned_data['img'] = '/nothing/'
#    form.save()

    # obj.image is the ImageField
    print(f)
#    print(data)
    print(img)

    return form
    
    #obj.image.save('imgfilename.jpg', ContentFile(data))


from rest_framework.viewsets import ModelViewSet

class Panel(ModelViewSet):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'panel.html'
 
    def get(self, request): 
        form = PostForm()
        return Response({'form': form})
    
    
    def put(self, request):
        pass

    def delete(self, request, format=None):
        if request.get_full_path() == '/delete/':
            if request.is_ajax and request.method == "DELETE":
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

        elif request.get_full_path() == '/panel/new_post':

            if request.POST:
                form = PostForm(request.POST, request.FILES)
                if form.is_valid():
                    post = form # instead of post = form.save(commit=False)
                    post.author = request.user 
                    form.save()

                    try:
                        post.save()
                        #form.save_m2m() override create for PostForm to support many to many relationship
                    except Exception as e:
                        print(e)
                        # only for test now, will use django-rest later
                        return Response({'form': form})

                    if form.cleaned_data['new_categories'] != '':
                        for cat in form.cleaned_data['new_categories'].split(','):
                            new_cat = CategorySerializer(name=cat, slug = cat)
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


from annoying.functions import get_object_or_None
def category_view(request, slug):
    category = Category.objects.get(slug = slug)
    articles = Article.objects.filter(categories__in = [category])
    return render(request, 'category.html', {'articles': articles})

from .models import Article_Category

def article_view(request, slug):
    article =  Article.objects.get(slug = slug)
    return render(request, 'Article.html', {'article': article})

@login_required(login_url='login')
def index(request):
    articles = Article.objects.all()
    return render(request, 'index.html', {'articles': articles})
