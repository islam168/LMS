from .views import CourseView, UserCourseView, CategoryList, CourseCreateView, CourseDetail, \
    CourseListView, CategoryDetail, RegisterAPI, LoginAPI, UserDetailView, MaterialViewSet, MaterialDetailViewSet
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from knox import views as knox_views

router = SimpleRouter()
router.register(r'usercourse', UserCourseView, basename='profile')
router.register('categories', CategoryList, basename='category')
router.register(r'materials', MaterialViewSet, basename='material')
urlpatterns = [
    path('', include(router.urls)),

    path('course_create/', CourseCreateView.as_view({'post': 'create'}), name='course_create'),
    path('course_page/<int:pk>/', CourseDetail.as_view(), name='course'),
    path('course/<int:pk>/', CourseView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='course_detail'),
    path('course_list/', CourseListView.as_view({'get': 'list'}), name='course_list'),

    path('category_detail/<int:pk>/', CategoryDetail.as_view(), name='category_detail'),
    path('categories/', CategoryList.as_view({'get': 'list', 'post': 'create'}), name='category_list'),

    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),

    path('material/', MaterialViewSet.as_view({'post': 'create'}), name='material'),
    path('material/<int:pk>/', MaterialDetailViewSet.as_view({'get': 'retrieve', 'put': 'update',
                                                              'delete': 'destroy'}), name='material_detail'),

    path('course_buy/', UserCourseView.as_view({'get': 'list', 'post': 'create'}), name='profile'),
    path('user_cabinet/<int:pk>/', UserDetailView.as_view(), name='user-detail'),

]
