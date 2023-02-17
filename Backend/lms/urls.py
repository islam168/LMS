from django.urls import path
from .views import *

urlpatterns = [
    path('course_list', CourseListView.as_view({'get': 'list'}), name='course_list'),  # Страница со списком курсов без возможности их создавать
    path('course', CourseView.as_view({'get': 'list',
                                           'post': 'create'}), name='course_list'),  # Страница со списком курсов с возможности их создавать
    path('course/<int:pk>', CourseView.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='course_detail'),
    path('categories/', CategoryList.as_view({'get': 'list',
                                              'post': 'create'}), name='category_list'),


]
