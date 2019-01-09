from django.db import models

# Create your models here.
from django.utils import timezone
from django.contrib.auth.models import User


class BlogArticles(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User,related_name="blog_posts")
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    class Meta():
        db_table = "blog_articles"
        ordering = ["-publish"]

    def _str_(self):
        return self.title


