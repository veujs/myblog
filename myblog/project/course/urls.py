from django.conf.urls import url
from django.views.generic import TemplateView
from .views import AboutView, CourseListView, ManagerCourseListView,CreateCourseView,DeleteCourseView

urlpatterns = [
    # url(r'^about/$', TemplateView.as_view(template_name="course/about.html")),
    url(r'^about/$', AboutView.as_view(),name="about"),
    url(r'^course-list/$', CourseListView.as_view(),name="course_list"),
    url(r'^manage-course/$',ManagerCourseListView.as_view(),name="manage_course"),
    url(r'^create-course/$',CreateCourseView.as_view(),name="create_course"),
    url(r'^delete-course/(?P<pk>\d+)/$',DeleteCourseView.as_view(),name="delete_course"),
]
















