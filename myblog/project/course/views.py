from django.shortcuts import render

# Create your views here.

from django.views.generic import TemplateView
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
        qs = super(CourseListView, self).get_queryset()
        return super(CourseListView, self).get_queryset().filter(user=User.objects.get(username="admin"))

class UserMixin:
    def get_queryset(self):
        return super(UserMixin, self).get_queryset().filter(user=self.request.user)

class UserCourseMixin(UserMixin):
    model = Course

class ManagerCourseListView(UserCourseMixin,ListView):
    context_object_name = "course"
    template_name = "course/manage/manage_course_list.html"








