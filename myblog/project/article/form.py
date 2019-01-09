from django import forms
from .models import ArticleColumn,ArticlePost


class ArticleColumnForm(forms.ModelForm):
    class Meta:
        model = ArticleColumn
        fields = ("column",)

class ArticlePostForm(forms.ModelForm):
    class Meta:
        model = ArticlePost
        fields = ["title","body"]


from .models import Comment
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["commentator","body"]


from .models import ArticleTag
class ArticleTagForm(forms.ModelForm):
    class Meta:
        model = ArticleTag
        fields = ('tag', )




