from .models import Category

from .urls import  urlpatterns, path

from .models import Category, Article
def articles(request):
    return {'articles' : Article.objects.all()}

def categories(request):
    return {'categories': Category.objects.all()}


