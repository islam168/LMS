from .views import *
from django.urls import path, include
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('course', CourseView, basename='course')
router.register('categories', CategoryList, basename='category')
urlpatterns = [
    path('', include(router.urls)),
    path('course_list/', CourseListView.as_view({'get': 'list'}), name='course_list'),
    path('category_detail/int:pk/', CategoryDetail.as_view(), name='category_detail'),
    path('categories/', CategoryList.as_view({'get': 'list',
                                              'post': 'create'}), name='category_list'),

]