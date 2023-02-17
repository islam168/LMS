from django.urls import path
from .views import *

urlpatterns = [
    path('course', CourseListView.as_view(), name='course_list'),
    path('course/<int:pk>', DetailView.as_view(), name='course_detail'),

]
