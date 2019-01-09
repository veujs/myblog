from django.shortcuts import render
from django.http import HttpResponse
from .models import ArticlePost
# from ..account.models import UserInfo
from django.core.paginator import PageNotAnInteger,Paginator,EmptyPage
# 以下为三个装饰器
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings
import redis
r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


from django.contrib.auth.models import User
def article_titles(request,username=None):
    """
    http://127.0.0.1:8000/article/list-article-titles/ 在未登录的条件下查看文章标题（也可理解为外部访问改文章）
    :param request:
    :return:
    """
    if username:
        # user = User.objects.filter(username=username) # @1@ 注意 如果在这里选择使用filter  那么返回的是一个列表{QuerySet 查询集}，下面必须使用user[0]
                                                    # 但是如果使用get，则下面直接使用user
                                                    # get返回的为模型类数据，filter返回的是查询集模型
        user = User.objects.get(username=username)# @2@
        articles_title = ArticlePost.objects.filter(author=user)

        try:
            # userinfo = user[0].userinfo  # @1@
            userinfo = user.userinfo# @2@
            # userinfo = UserInfo.objects.get(user=user)
            pass
        except:
            userinfo = None
        # print("******************************************")
        # print(articles_title)
        # print("userinfo:",userinfo)
        # print("userinfo-type:", type(userinfo))
        # print("user:",user)
        # print("user-type:",type(user))
    else:
        articles_title = ArticlePost.objects.all()

    # articles_title = ArticlePost.objects.all()
    paginator = Paginator(articles_title,10)
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
    if username:
        return render(request, "article/list/author_articles.html", {"articles":articles,
                                                                     "page":current_page,
                                                                     "userinfo":userinfo,
                                                                     "user":user})

    return render(request, "article/list/article_titles.html", {"articles":articles,
                                                                "page": current_page})

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
# import json
from .models import Comment
from .form import CommentForm
# @login_required(login_url='/account/login')
def article_detail(request,id,slug):
    article = get_object_or_404(ArticlePost,id=id,slug=slug)
    total_views = r.incr("article:{}:views".format(article.id))
    r.zincrby(name='article_ranking',value=article.id,amount=1)  # name  acount value  根据amount所设定的步长增加有序集合name中value对应的数值
                            # article_ranking为redis数据库的一种数据类型 有序集合  （zset）
                            # 注意有序集合中每一行 row（行数） value（键） score（分数）
    article_ranking = r.zrange('article_ranking',0,-1,desc=True)[:3]   # 得到有序集合article_ranking中score分数排序前3 的对象
     # 注意  上边得到的article_ranking位bytes类型，通过下面的函数将其转化为数值型(int)
    article_ranking_ids = [int(id) for id in article_ranking] # 列表推导式  将article_ranking的id组成列表
    most_viewed = list(ArticlePost.objects.filter(id__in=article_ranking_ids))  # 查询出article_ranking中的在ArticlePost的文章对象
    most_viewed.sort(key=lambda x:article_ranking_ids.index(x.id))
    # d = json.loads(r.get(name="article:1:views"))
    # print("article:1:views:",d)
    # print("*****article_detail******")
    # print(type(article_ranking))
    # print(article_ranking)
    # print(type(article_ranking_ids))
    # print(article_ranking_ids)

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.save()
    else:
        comment_form = CommentForm()

    # wzp获取评论最多的前三个
    all_articles = ArticlePost.objects.all()
    article_comment_dict = {}
    for one_article in all_articles:
        article_comment_dict[one_article.id] = one_article.comments.count()
    article_comment_range = sorted(article_comment_dict.items(),key=lambda e:e[1],reverse=True)[:3]
    article_comment_range1 = [ArticlePost.objects.get(id=mm[0]) for mm in article_comment_range]
    # print("%%%%%%%%%%%%%%%%")
    # print(article_comment_dict)
    # print(article_comment_range)
    # print(article_comment_range1)


    return render(request,'article/list/article_detail.html',{
        "article":article,
        "total_views":total_views,
        "most_viewed":most_viewed,
        "comment_form":comment_form,
        "article_comment_range1":article_comment_range1
    })


@csrf_exempt
@require_POST
@login_required(login_url="/account/login")
def like_article(request):
    article_id = request.POST.get("id")
    action = request.POST.get("action")
    if article_id and action:
        try:
            article = ArticlePost.objects.get(id=article_id)
            if action == "like":
                article.users_like.add(request.user)
                return HttpResponse("1")
            else:
                article.users_like.remove(request.user)
                return HttpResponse("2")
        except:
            return HttpResponse("no")

























