from django.shortcuts import render

# Create your views here.

from django.shortcuts import get_object_or_404, HttpResponseRedirect, get_list_or_404
from .models import  Category, Article
from django.contrib.auth.models import User
from django import forms
from .forms import PostForm, CategoryForm
from django.db import IntegrityError

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

@login_required(login_url='login')
def post_success(request):
    return render(request, "post_success.html")
from django.contrib.auth import logout

def sign_out(request):
    if request.user.is_authenticated:
        logout(request)
        return render(request, "logged_out.html")
    else:
        return HttpResponseRedirect('login')


from .models import Articles_Categories


@login_required(login_url='login')
def panel(request):
    if request.get_full_path() == '/delete/':
        if request.is_ajax and request.method == "DELETE":
            print("successfully deleted")


    if request.get_full_path() == '/panel/settings':
        # just showing categories for now
        if  request.is_ajax and request.method == "DELETE":
            print("hello")

        if request.method == 'POST':
            form = CategoryForm(request.POST)
            if form.is_valid():
                form.save(commit=True) 
                success_message = f"Category {form.cleaned_data['name']} successfuly added" 
                form = CategoryForm()
                return render(request, 'panel.html', {'settings': True, 'category_form' : form, 'success_message' :success_message})
            else:
                return render(request, 'panel.html', {'settings': True, 'category_form': form})
        
        form = CategoryForm()
        return render(request, 'panel.html', {'settings': True, 'category_form': form})

    elif request.get_full_path() == '/panel/new_post':
        form = PostForm()
        return render(request, 'panel.html', {'form': form})

    if request.method == 'POST' and request.POST:
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            try:
                post.save()
                form.save_m2m()
            except Exception as e:
                return render(request, 'panel.html', {'form': form})
                 
            if form.cleaned_data['new_categories'] != '':
                for cat in form.cleaned_data['new_categories'].split(','):
                    new_cat = Category(name=cat, slug = cat)
                    new_cat.save()
                    try:
                        post.save()
                        article_category = Articles_Categories(category_id = new_cat.id,
                            article_id = post.id)
                        article_category.save()
                        print(article_category.category.id, article_category.article.id)
                        print(new_cat.id)                             
                    except IntegrityError as e:
                        err = f"Category: {cat} exists."
                        return render(request, 'panel.html', {'form': form, 'error': err})
                 
            return HttpResponseRedirect("/panel/new_post/success")
        else:
                
            return render(request, 'panel.html', {'form': form})
    else:
        form = PostForm()
        return render(request, 'panel.html', {'form': form})

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

from .models import Articles_Categories

def article_view(request, slug):
    article =  Article.objects.get(slug = slug)
    return render(request, 'Article.html', {'article': article})

@login_required(login_url='login')
def index(request):
    articles = Article.objects.all()
    return render(request, 'index.html', {'articles': articles})
