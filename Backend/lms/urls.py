from .views import *
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import RegisterAPI, LoginAPI
from knox import views as knox_views

router = SimpleRouter()
router.register('course', CourseView, basename='course')
router.register('categories', CategoryList, basename='category')
urlpatterns = [
    path('', include(router.urls)),
    path('course_list/', CourseListView.as_view({'get': 'list'}), name='course_list'),
    path('category_detail/int:pk/', CategoryDetail.as_view(), name='category_detail'),
    path('categories/', CategoryList.as_view({'get': 'list',
                                              'post': 'create'}), name='category_list'),
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),


]