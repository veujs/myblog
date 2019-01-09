from django.db import models
from django.contrib.auth.models import User
# Create your models here.


# 文章栏目数据模型
class ArticleColumn(models.Model):
    user = models.ForeignKey(User, related_name="article_column")
    column = models.CharField(max_length=200)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return  self.column


# 文章标签类
class ArticleTag(models.Model):
    author = models.ForeignKey(User, related_name="tag")
    tag = models.CharField(max_length=500)

    def __str__(self):
        return self.tag


from django.utils import timezone
from slugify import slugify
from django.core.urlresolvers import reverse
# 文章发布数据模型
class ArticlePost(models.Model):
    author = models.ForeignKey(User, related_name="article") # related_name的作用关联User数据库
                                        #      例如：post1 = ArticlePost.objects.get(id=1)
                                        # post1.author----->得到的是对应的user对象--也就是User类
                                        #  也就是说如果给    ArticlePost 的属性author赋值的话，必须以User对象的形式赋值

    title = models.CharField(max_length=200)
    slug = models.SlugField (max_length=500)
    column = models.ForeignKey(ArticleColumn,related_name="article_column")
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now()) # 文章发布的时间和日期
    updated = models.DateTimeField(auto_now=True)

    users_like = models.ManyToManyField(User, related_name="articles_like", blank=True)

    article_tag = models.ManyToManyField(ArticleTag, related_name='article_tag', blank=True)


    class Meta:
        ordering = ["title"] # 表中数据按照title字段来排序显示
        index_together = (("id","slug"),) #对数据库中这两个字段建立索引

    def __str__(self):
        return self.title

    def save(self,*args,**kargs):
        self.slug = slugify(self.title)
        super(ArticlePost, self).save(*args, **kargs)

    def get_absolute_url(self):
        return reverse("article:article_detail",args=[self.id,self.slug])

    def get_url_path(self):
        return reverse("article:list_article_detail",args=[self.id,self.slug])


class Comment(models.Model):
    article = models.ForeignKey(ArticlePost,related_name="comments")
    commentator = models.CharField(max_length=90)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)
    def __str__(self):
        return "Comment by {0} on {1}".format(self.commentator.username,self.article)


