from django.contrib import admin
from .models import UserProfile,UserInfo
from django.contrib.auth.models import User
# Register your models here.

class UserProfileAdmin(admin.ModelAdmin):
    # class UserInfo(admin.TabularInline):
    #     model = User
    #     extra = 2
    # inlines = [UserInfo]

    list_display = ["id","user","birth","phone"]
    list_filter = ["birth","phone","user"]
admin.site.register(UserProfile,UserProfileAdmin)


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ["school","company","profession","address","aboutme","user"]
    list_filter = ["school","profession"]

admin.site.register(UserInfo,UserInfoAdmin)