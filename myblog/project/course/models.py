from django.db import models

# Create your models here.


from django.contrib.auth.models import User
from slugify import slugify
from django.utils import timezone
class Course(models.Model):
    user = models.ForeignKey(User,related_name="course_user")
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now=timezone.now())

    student = models.ManyToManyField(User,related_name="courses_joined",blank=True)

    class Meta:
        ordering = ("-created",)
    def save(self,*args,**kargs):
        self.slug = slugify(self.title)
        super(Course, self).save(*args,**kargs)

    def __str__(self):
        return self.title




# 下面为发布和课程学习内容的数据模型
from .fields import OrderField
def user_directory_path(instance,filename): # instance引用是Lesson实例，filename为得到的文件名
    return "courses/user_{0}/{1}".format(instance.user.id,filename)

class Lesson(models.Model):
    user = models.ForeignKey(User,related_name="lesson_user")
    course = models.ForeignKey(Course,related_name="lesson")
    title = models.CharField(max_length=200)
    # video = models.FileField(upload_to="videos")
    video = models.FileField(upload_to=user_directory_path)
    description = models.TextField(blank=True)
    # attach = models.FileField(blank=True,upload_to="attachs")
    attach = models.FileField(blank=True,upload_to=user_directory_path)
    created = models.DateTimeField(auto_now=True)
    order = OrderField(blank=True,for_fields=['course'])
    # order用于存储某内容在相应的课程标题Courselves中的序号(序号从0开始)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return '{}.{}'.format(self.order,self.title)








