from django import forms
from django.contrib.auth.models import User
from .models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(max_length=12)
    password = forms.CharField(widget=forms.PasswordInput)

# 定义用户注册表单类RegistrationForm---对应数据模型User
class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    # 有时候我们不必在表单中向数据模型中的所有宇段赋值（或者不需要把数据库表中所有的字段写入数据）
    class Meta:  # 内部类   注意：表单类中的属性和数据模型类中的属性一一对应
        model = User  # 指定本表单的内容会写到哪个数据库表中的哪些记录里面
        fields = ["username", "email"]  # 这两个属性在User中都存在，并且不需要为其复制

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("密码不匹配")
        return cd['password2']

# 定义用户注册相关信息表单类UserProfileForm---对应数据模型UserProfile
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["phone", "birth"]

# 定义用户个人信息表单类UserInfoForm---对应数据模型UserInfo
from .models import UserInfo
class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo  # 表明UserInfoForm表单类针对的是UserInfo数据模型类
        fields = ["school", "company", "profession", "address", "aboutme"]  # 要添加的属性或者字段
        # exclude = ['photo']
# 定义用户信息表单类UserForm---对应数据模型User--auth_user
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email"]
