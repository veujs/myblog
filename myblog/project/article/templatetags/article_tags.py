from django import template

register = template.Library()
# from article.models import ArticlePost
from ..models import ArticlePost


@register.simple_tag
def total_articles():
    return ArticlePost.objects.count()

@register.simple_tag
def author_total_articles(user):
    return user.article.count()
    # return ArticlePost.objects.filter(author=user).count()

@register.inclusion_tag('article/list/latest_articles.html')
def latest_articles(n=5):
    latest_articles = ArticlePost.objects.order_by("-created")[:n]
    return {"latest_articles":latest_articles}

from django.db.models import Count
@register.assignment_tag # 用于声明下面函数为自定义的assignment_tag 类型的标签函数
def most_commented_articles(n=3):
    return ArticlePost.objects.annotate(total_comments=Count('comments')).order_by("-total_comments")[:n]

from django.utils.safestring import mark_safe
import markdown
@register.filter(name='markdown')
def markdown_filter(text):
    return mark_safe(markdown.markdown(text))
























