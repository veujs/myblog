from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.contrib.auth.decorators import login_required
from .models import ArticleColumn

from .form import ArticleColumnForm
from django.views.decorators.csrf import csrf_exempt
@login_required(login_url='/account/login/') # 装饰器函数，来判断用户是否登录
@csrf_exempt   # 使用装饰器来解决表单提交的时候csrf的问题，这个方法只用在views视图函数当中
def article_column(request):
    """
    在http://127.0.0.1:8000/article/article-column/显示栏目详情
    :param request:
    :return:
    """
    if request.method == "GET":
        columns = ArticleColumn.objects.filter(user=request.user)
        column_form = ArticleColumnForm()
        return render(request,'article/column/article_column.html',{"columns":columns,"column_form":column_form})
    elif request.method == "POST":
        column_name = request.POST.get("column") # 表单类里面可操作的字段仅仅为column
        columns = ArticleColumn.objects.filter(user=request.user,column=column_name)
        if columns: # 如果该用户已经有该栏目名称
            return HttpResponse("2")
        else:
            ArticleColumn.objects.create(user=request.user,column=column_name)
            return HttpResponse("1")



from django.views.decorators.http import require_POST
@login_required(login_url='/account/login/') # 装饰器函数，来判断用户是否登录
@require_POST # 这个装饰器的目的是保证此时凸函数只接受通过POST方式提交的数据
@csrf_exempt   # 使用装饰器来解决表单提交的时候csrf的问题，这个方法只用在views视图函数当中
def rename_article_column(request):
    """
    在http://127.0.0.1:8000/article/article-column/修改栏目名称
    :param request:
    :return:
    """
    column_name = request.POST["column_name"]
    column_id = request.POST.get("column_id")
    try:
        line = ArticleColumn.objects.get(id=column_id)
        line.column = column_name
        line.save()
        return HttpResponse("1")
    except:
        return HttpResponse("0")

@login_required(login_url='/account/login/') # 装饰器函数，来判断用户是否登录
@require_POST # 这个装饰器的目的是保证此时凸函数只接受通过POST方式提交的数据
@csrf_exempt   # 使用装饰器来解决表单提交的时候csrf的问题，这个方法只用在views视图函数当中
def delete_article_column(request):
    """
     在http://127.0.0.1:8000/article/article-column/删除栏目
    :param request:
    :return:
    """
    column_id = request.POST.get("column_id")
    try:
        line = ArticleColumn.objects.get(id=column_id)
        line.delete()
        # line.save()  # 不需要加save（）语句，直接在数据库中删除了，加上会出问题
        return HttpResponse("1")
    except:
        HttpResponse("2")

from .form import ArticlePostForm
import json
@login_required(login_url='/account/login')
@csrf_exempt
def article_post(request):
    """
    http://127.0.0.1:8000/article/article-post/进行文章发布
    :param request:
    :return:
    """
    if request.method == "POST":
        article_post_form = ArticlePostForm(data=request.POST)
        print(article_post_form)
        print(article_post_form.is_valid)
        if article_post_form.is_valid():

            print(article_post_form)
            cd = article_post_form.cleaned_data
            try:
                new_article = article_post_form.save(commit=False)
                new_article.author = request.user
                new_article.column = request.user.article_column.get(id=request.POST['column_id'])
                new_article.save()
                tags = request.POST['tags']
                if tags:
                    for atag in json.loads(tags):
                        tag = request.user.tag.get(tag=atag)
                        new_article.article_tag.add(tag)

                return HttpResponse("1")
            except:
                return HttpResponse("2")
        else:
            return HttpResponse("3")
    else:
        article_post_form = ArticlePostForm()
        article_columns = request.user.article_column.all()
        article_tags = request.user.tag.all()
        return render(request, "article/column/article_post.html",
                      {
                        "article_post_form": article_post_form,
                       "article_columns": article_columns,
                       "article_tags":article_tags
                       })



from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger # 分页功能所需要的
from .models import ArticlePost
def article_list(request):
    """
    http://127.0.0.1:8000/article/article-list/文章列表,并且叫列表中的文章全部分页显示
    :param request:
    :return:
    """
    article_list = ArticlePost.objects.filter(author=request.user)
    paginator = Paginator(article_list,3)
    page = request.GET.get("page")
    try:
        current_page = paginator.page(page)
        articles = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        articles = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        articles = current_page.object_list
    return render(request,'article/column/article_list.html',{'articles':articles,"page":current_page})


from django.shortcuts import get_object_or_404
@login_required(login_url='/account/login')
def article_detail(request,id,slug):
    article = get_object_or_404(ArticlePost,id=id,slug=slug)
    return render(request,'article/column/article_detail.html',{"article":article})





@login_required(login_url='/account/login')
@csrf_exempt
def delete_article(request):
    """
    http://127.0.0.1:8000/article/article-list/删除文章列表中的某一篇文章
    :param request:
    :return:
    """
    article_id = request.POST["article_id"]
    try:
        article_del = ArticlePost.objects.get(id=article_id)
        article_del.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")


@login_required(login_url='/account/login')
@csrf_exempt

def redit_article(request,article_id):
    """
    http://127.0.0.1:8000/article/redit-article/1/ 编辑对应列表中的文章并进行保存发布
    :param request:
    :param article_id:
    :return:
    """
    if request.method == "GET":
        article_columns = ArticleColumn.objects.filter(user_id=request.user.id) # 获取当前用户的所有栏目
        article = ArticlePost.objects.get(id=article_id) # 获取要修改的文章对象
        this_article_column = article.column # 获取改文章所在的栏目
        this_article_form = ArticlePostForm(initial={"title":article.title}) # 再次初始化一个文章发布表单类，用于再次编辑

        return render(request,'article/column/redit_article.html',{"article":article,
                                                                   "article_columns":article_columns,
                                                                   "this_article_form":this_article_form,
                                                                   "this_article_column":this_article_column
                                                                   })
    elif request.method == "POST":
        #  title  body  column
        redit_article = ArticlePost.objects.get(id=article_id)
        try:
            redit_article.column = ArticleColumn.objects.get(id=request.POST["column_id"])
            redit_article.title = request.POST["title"]
            redit_article.body = request.POST["body"]
            redit_article.save()
            return HttpResponse("1")
        except:
            return HttpResponse("2")



from .form import ArticleTagForm
from .models import ArticleTag
@login_required(login_url='/account/login')
@csrf_exempt
def article_tag(request):
    if request.method == "GET":
        article_tags = ArticleTag.objects.filter(author=request.user)
        article_tag_form = ArticleTagForm()
        return render(request, "article/tag/tag_list.html", {"article_tags":article_tags, "article_tag_form":article_tag_form})

    if request.method == "POST":
        tag_post_form = ArticleTagForm(data=request.POST)
        if tag_post_form.is_valid():
            try:
                new_tag = tag_post_form.save(commit=False)
                new_tag.author = request.user
                new_tag.save()
                return HttpResponse("1")
            except:
                return HttpResponse("the data cannot be save.")
        else:
            return HttpResponse("sorry, the form is not valid.")

@login_required(login_url='/account/login')
@require_POST
@csrf_exempt
def del_article_tag(request):
    tag_id = request.POST['tag_id']
    try:
        tag = ArticleTag.objects.get(id=tag_id)
        tag.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")











