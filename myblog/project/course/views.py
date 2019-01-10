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

    def get_queryset(self):
        return super(CourseListView, self).get_queryset().filter(user=User.objects.get(username="admin"))

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















