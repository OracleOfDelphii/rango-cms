from django.core.exceptions import ObjectDoesNotExist
from django.utils.text import slugify
from django.contrib.auth.views import LoginView
from django.db.utils import IntegrityError
from django.shortcuts import redirect 
from .models import  Category, Article
from .forms import PostForm
from django.contrib.auth.views import LoginView    
from django.utils import timezone
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView

class Panel(TemplateView):
    
    template_name = 'panel.html'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = Article.objects.all()
        context['categories'] = Category.objects.all()
        return context
    
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().get(request, *args, **kwargs)

from django.views.generic.edit import  CreateView, UpdateView, DeleteView

class NewPostView(CreateView):
    template_name = 'panel.html'
    form_class = PostForm
    context_object_name = 'form'
    model =  Article
    success_url ="/success/" # posts list url

    def form_valid(self, form):
        article = form.save(commit=False)
        article.save()
        for category in form.cleaned_data.get('new_categories').split(','):
            try:
                new_cat = Category.objects.get_or_create(name=category, slug=slugify(category))[0]
                article.categories.add(new_cat)
            except (IntegrityError,ValueError) as e:
                print(e)
                
        form.save_m2m()
        
        return super().form_valid(form)

 
    
class SuccessView(TemplateView):
    template_name = 'post_success.html'
    

class EditPostView(UpdateView):
    form_class = PostForm
    template_name = 'panel.html'
    context_object_name = 'form'
    model = Article
    success_url = r'/success/'
 

class ListArticles(TemplateView):
    template_name = 'panel.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = Article.objects.all()
        return context
      
class ListCategories(TemplateView):
    template_name = 'panel.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context 

class DeletePostView(DeleteView):
    model = Article
    template_name='article_confirm_delete.html'
    success_url = reverse_lazy('posts')
    

class IndexView(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = Article.objects.filter(date__lte=timezone.now(), is_published=True).order_by('-date')
        context['categories'] = Category.objects.all()
        return context
    
class ViewArticles(TemplateView):
    template_name = 'articles.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs.get('category_slug'):
            try:
                category = Category.objects.get(slug=self.kwargs.get('category_slug'))
                
                print(timezone.now())
                context['articles'] = Article.objects.filter(categories__in=[category], date__lte=timezone.now(), is_published=True).order_by('-date')
                
                context['categories'] = Category.objects.all()
                
            except ObjectDoesNotExist:
                context['articles'] = Article.objects.all()
 
        context['categories'] = Category.objects.all()
        
        
        return context
    
    
class ViewArticle(TemplateView):
    template_name = 'article.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article'] = Article.objects.get(slug=self.kwargs.get('article_slug'), date__lte=timezone.now(), is_published=True)
        context['categories'] = Category.objects.all()
        
        
        return context

class Login(LoginView):
    template_name = 'login.html'