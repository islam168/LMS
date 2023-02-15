from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateAPIView
from .models import Course
from .serializers import CourseSerializer


class CourseListView(ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class DetailView(RetrieveUpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


