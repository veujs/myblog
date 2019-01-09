from django.contrib import admin

# Register your models here.


from .models import ArticleColumn
class ArticleColumnAdmin(admin.ModelAdmin):
    list_display = ["user","column","created"]
    list_filter = ["column","created","user"]
admin.site.register(ArticleColumn,ArticleColumnAdmin)