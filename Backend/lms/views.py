from rest_framework import filters, viewsets
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from .models import Course, Category
from .serializers import CourseSerializer, CategorySerializer, CourseListSerializer
from django_filters.rest_framework import DjangoFilterBackend



class CourseListView(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseListSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ('title', '=category__category_name')


# View для страницы со списком курсов с возможности их создавать
class CourseView(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CategoryList(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetail(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CourseSerializer


from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from .serializers import UserSerializer
from rest_framework.generics import CreateAPIView, UpdateAPIView

User = get_user_model()

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

class UserCreateView(CreateAPIView):
    serializer_class = UserSerializer

class UserUpdateView(UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'id'

