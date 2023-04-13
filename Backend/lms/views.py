from rest_framework import filters, viewsets
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from .models import Course, Category, UserProfile, Course, CourseEnrollment
from .serializers import CourseSerializer, CategorySerializer, CourseListSerializer, UserSerializer, RegisterSerializer, \
    LoginSerializer, CourseCreateSerializer,UserPfofileSerialezer
from django_filters.rest_framework import DjangoFilterBackend
from knox.models import AuthToken
from rest_framework import permissions
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView



class CourseListView(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseListSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ('title', '=category__category_name')


# View для страницы со списком курсов с возможности их создавать
class CourseView(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class CourseCreateView(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseCreateSerializer

class CourseDetail(RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class CategoryList(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetail(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CourseSerializer



User = get_user_model()

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })

class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        _, token = AuthToken.objects.create(user)
        return Response({
            "user": UserSerializer(user).data,
            "token": token
        })

class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'
    permission_classes = (permissions.IsAuthenticated,)



# система CRUD
# создание
@api_view(['POST'])
def create_course(request):
    serializer = CourseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# читать
class CourseList(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class CourseDetail(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


# Редактировать
@api_view(['PUT'])
def update_course(request, pk):
    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = CourseSerializer(course, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# удалить
@api_view(['DELETE'])
def delete_course(request, pk):
    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    course.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)




# class UserProfileViewSet(viewsets.ModelViewSet):
#     """creating and updation profiles"""
#
#     serializer_class = serializers.UserProvileSerailezer


@api_view(['POST'])
def enroll_user_in_course(request):
    user_id = request.data.get('user_id')
    course_id = request.data.get('course_id')

    user_profile = UserProfile.objects.get(name='user_name')
    course = Course.objects.get(id=course_id)

    enrollment = CourseEnrollment(user_profile=user_profile, course=course)
    enrollment.save()

    return Response({'status': 'success'})



@api_view(['GET'])
def courses_taken_by_user(request, user_id):
    user_profile = UserProfile.objects.get(id=user_id)
    courses_taken = user_profile.courses_taken.all()

    course_list = []
    for course in courses_taken:
        course_dict = {
            'id': course.id,
            'name': course.name,
            'start_time': course.start_time,
            'end_time': course.end_time,
        }
        course_list.append(course_dict)

    return Response(course_list)
