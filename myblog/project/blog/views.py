from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
# Create your views here.


def index(request):
    return HttpResponse("项目开始")


from .models import BlogArticles
# from django.contrib.auth.models import User
def blog_title(request):
    blogs = BlogArticles.objects.all()
    return render(request,'blog/title.html',{"blogs":blogs})

def blog_article(request,article_id):
    article = get_object_or_404(BlogArticles,id=article_id)
    # article = BlogArticles.objects.get(id=article_id)
    pub = article.publish
    return render(request,'blog/content.html',{"article":article
                                               ,"publish":pub})


