from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate,login
from .form import LoginForm,RegistrationForm,UserProfileForm
from django.http import HttpResponseRedirect
# Create your views here.

def user_login(request):
    """
    用户登录
    :param request:
    :return:
    """
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid(): # 判断设置的参数是否合法
            cd = login_form.cleaned_data # 参数合法后，才会在cleaned_data中将提交的数据缓存下来
            user = authenticate(username=cd['username'],password=cd['password']) # 验证是否为本网站的用户
            if user:
                login(request,user)
                # return HttpResponse("验证成功")
                return redirect('/home/')
            else:
                return HttpResponse("账号或者密码错误！")
        else:
            return HttpResponse("验证无效！")
    elif request.method == "GET":
        login_form= LoginForm()
        return render(request,'account/login.html',{'form':login_form})

def register(request):
    """
    新用户注册
    :param request:
    :return:
    """
    if request.method == "POST":
        user_form = RegistrationForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        if user_form.is_valid() * userprofile_form.is_valid():
            new_user = user_form.save(commit=False) # commit=False告诉Django先不提交到数据库.
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save() # 发送到数据库

            new_profile = userprofile_form.save(commit=False)
            new_profile.user = new_user
            new_profile.save()

            UserInfo.objects.create(user=new_user) # 在account_info数据表中写入该用户ID 的信息

            # return HttpResponse("成功")
            return redirect(reverse("account:user_login"))
        else:
            return HttpResponse("对不起，无法注册")
    else:
        user_form = RegistrationForm()
        userprofile_form = UserProfileForm()
        return render(request,"account/register.html",{"form":user_form,
                                                       "profile":userprofile_form})



from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserInfo,UserProfile
@login_required(login_url='/account/login/') # 装饰器函数，来判断用户是否登录
def myself(request):
    """
    个人信息展示
    :param request:
    :return:
    """
    user = User.objects.get(username=request.user.username)
    userprofile = UserProfile.objects.get(user=user)
    userinfo = UserInfo.objects.get(user=user)
    return render(request,'account/myself.html',{"user":user,"userprofile":userprofile,"userinfo":userinfo})

from .form import UserProfileForm,UserForm,UserInfoForm
def myself_edit(request):
    """
    个人详细信息编辑界面
    :param request:
    :return:
    """
    user = User.objects.get(username=request.user.username)
    userprofile = UserProfile.objects.get(user=user)
    userinfo = UserInfo.objects.get(user=user)

    if request.method == "POST":
        user_form = UserForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        userinfo_form = UserInfoForm(request.POST)
        if user_form.is_valid() * userprofile_form.is_valid() * \
                userinfo_form.is_valid():
            user_cd = user_form.cleaned_data
            userprofile_cd = userprofile_form.cleaned_data
            userinfo_cd = userinfo_form.cleaned_data

            user.email = user_cd["email"]
            userprofile.phone = userprofile_cd["phone"]
            userprofile.birth = userprofile_cd["birth"]
            userinfo.school = userinfo_cd["school"]
            userinfo.company = userinfo_cd["company"]
            userinfo.profession = userinfo_cd["profession"]
            userinfo.address = userinfo_cd["address"]
            userinfo.aboutme = userinfo_cd["aboutme"]

            userimage = userinfo.photo
            # request.FILES["img"] = userinfo.photo
            # usrimg = request.FILES.get('img')
            userinfo.photo = "11"

            user.save()
            userprofile.save()
            userinfo.save()


            userinfo.photo = userimage
            userinfo.save()
        return HttpResponseRedirect('/account/my-information/')
    else:
        user_form = UserForm(instance=request.user)
        userprofile_form = UserProfileForm(initial={"birth":userprofile.birth,"phone":userprofile.phone})
        userinfo_form = UserInfoForm(initial={
            "school":userinfo.school,
            "company": userinfo.company,
            "profession": userinfo.profession,
            "address": userinfo.address,
            "aboutme": userinfo.aboutme,
        })
        return render(request,'account/myself_edit.html',{
            "user_form":user_form,
            "userprofile_form": userprofile_form,
            "userinfo_form": userinfo_form
        })

@login_required(login_url="/account/login/")
def my_image(request):
    if request.method == "POST":
        img = request.POST.get("img")
        userinfo = UserInfo.objects.get(user=request.user.id)
        userinfo.photo = img
        userinfo.save()
        return HttpResponse("1")
    else:
        return render(request,'account/imagecrop.html',{})
























