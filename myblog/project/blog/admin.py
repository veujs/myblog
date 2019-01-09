from django.contrib import admin

# Register your models here.
from .models import BlogArticles


# @admin.register(BlogArticles) # 使用装饰器进行注册
class BlogArticlesAdmin(admin.ModelAdmin):
    # class StudentsInfo(admin.TabularInline):
    #     model = Students
    #     extra = 2
    # inlines = [StudentsInfo]
    # 列表页的属性
    list_display = ['id','title','author','publish']# 显示字段
    list_display_links = ('id', 'title')#设置哪些字段可以点击进入编辑界面
    list_filter = ('title',"author") # 显示过滤器,!需要注意 外键不可用于列表页属性的过滤器
    search_fields = ['title'] # 搜索字段
    list_per_page = 5
    # raw_id_fields = ["author"] # 只适用于外键，会显示外键的详细信息
    date_hierarchy = "publish"  # 详细时间分层筛选　
    ordering = ['publish','author']   # ordering设置默认排序字段，负号表示降序排序

    # 添加修改页属性
    # fields = ['ggirlnum','gboynum','gname','isDelete','gdate']
    # fieldsets = [
    #     ('base',{"fields":['gname','gdate','isDelete']}),
    #     ('num',{"fields":['ggirlnum','gboynum']})
    # ]
admin.site.register(BlogArticles,BlogArticlesAdmin)