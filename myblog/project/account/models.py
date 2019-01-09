from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):
    # user = models.CharField(max_length=)
    user = models.OneToOneField(User,unique=True) # 通过user字段来声明UserProfile类与User类之间的关系以是一对一的
    birth = models.DateField(blank=True,null=True)
    phone = models.CharField(max_length=20,null=True)
    def __str__(self):
        return  'user:{}'.format(self.user.username)

class UserInfo(models.Model):
    user = models.OneToOneField(User,unique=True)
    school = models.CharField(max_length=100,blank=True)
    company = models.CharField(max_length=100,blank=True)
    profession = models.CharField(max_length=100,blank=True)
    address = models.CharField(max_length=100,blank=True)
    aboutme = models.TextField(blank=True)
    photo = models.ImageField(blank=True)

    def __str__(self):
        return  'user:{}'.format(self.user.username)

