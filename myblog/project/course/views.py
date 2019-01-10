from django.shortcuts import render
from braces.views import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic.base import TemplateResponseMixin
# Create your views here.

from django.views.generic import TemplateView,DeleteView
class AboutView(TemplateView):
    template_name = "course/about.html"

from django.contrib.auth.models import User
from django.views.generic import ListView
from .models import Course
class CourseListView(ListView):
    model = Course
    context_object_name = "courses"
    template_name = "course/course_list.html"

    # def get_queryset(self):
        # return super(CourseListView, self).get_queryset().filter(user=User.objects.get(username="admin"))
        # return super(CourseListView, self).get_queryset().filter(user=User.objects.get(username="admin"))

class UserMixin:
    def get_queryset(self):
        return super(UserMixin, self).get_queryset().filter(user=self.request.user)

class UserCourseMixin(UserMixin,LoginRequiredMixin):
    model = Course
    login_url = "/account/login/"

class ManagerCourseListView(UserCourseMixin,ListView):
    context_object_name = "courses"
    template_name = "course/manage/manage_course_list.html"



from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView
from django.shortcuts import redirect
from .form import CreateCourseForm

class CreateCourseView(UserCourseMixin,CreateView):
    fields = ["title","overview"]
    template_name = "course/manage/create_course.html"

    def post(self, request, *args, **kwargs):
        form = CreateCourseForm(data=request.POST)
        if form.is_valid():
            new_course = form.save(commit=False)
            new_course.user = self.request.user
            new_course.save()
            return redirect("course:manage_course")
        return self.render_to_response({"form":form})

import json
class DeleteCourseView(UserCourseMixin,DeleteView):
    # template_name = "course/manage/delete_course_confirm.html"
    success_url = reverse_lazy("course:manage_course")
    def dispatch(self, *args, **kwargs):
        resp = super(DeleteCourseView, self).dispatch(*args, **kwargs)
        if self.request.is_ajax():
            response_data = {"result":"ok"}
            return HttpResponse(json.dumps(response_data),content_type="application/json")
        else:
            return resp


from .models import Lesson
from .form import CreateLessonForm
from django.views import View
class CreateLessonView(LoginRequiredMixin,View):
    model = Lesson
    login_url = "/account/login/"
    def get(self,request,*args,**kwargs):
        form = CreateLessonForm(user=self.request.user)
        return render(request,'course/manage/create_lesson.html',{"form":form})

    def post(self,request,*args,**kwargs):
        form = CreateLessonForm(self.request.user,request.POST,request.FILES)
        if form.is_valid():
            new_lesson = form.save(commit=False)
            new_lesson.user = self.request.user
            new_lesson.save()
            return redirect("course:manage_course")

class ListLessonView1(LoginRequiredMixin,ListView):
    model = Lesson
    login_url = "/account/login/"
    context_object_name = "lessons"
    template_name = "course/manage/course_lesson_list.html"

    def get_queryset(self,**kwargs):
        return super(ListLessonView1, self).get_queryset().filter(course=Course.objects.get(id=self.kwargs["id"]))


from django.shortcuts import get_object_or_404
class ListLessonView2(LoginRequiredMixin,TemplateResponseMixin,View):
    login_url = "/account/login/"
    template_name = "course/manage/course_lesson_list.html"

    def get(self,request,course_id):
        course = get_object_or_404(Course,id=course_id)
        return self.render_to_response({"course":course})


class DetailLessonView(LoginRequiredMixin,ListView):

    model = Lesson
    login_url = "/account/login/"
    context_object_name = "lesson"
    template_name = "course/manage/detail_lesson.html"

    def get_queryset(self,**kwargs):
        return super(DetailLessonView, self).get_queryset().get(id=self.kwargs["id"])


class StudentListLessonView(ListLessonView2):
    template_name = "course/slist_lessons.html"

    def post(self,request,*args,**kwargs):
        course = Course.objects.get(id=self.kwargs["course_id"])
        course.student.add(self.request.user)
        return HttpResponse("ok")



