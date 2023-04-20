from rest_framework import serializers
from .models import Course, Category, UserCourse, Material
import datetime
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model, authenticate
from rest_framework.serializers import ModelSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name']


class CourseSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'content', 'category', 'price', 'discount_confirmation', 'discount', 'start_day',
                  'end_day']

    def update(self, instance, validated_data):
        if self.context['request'].method == 'PUT':
            discount = int(instance.discount)
            instance.price = validated_data.get('price')
            instance.discount_confirmation = validated_data.get('discount_confirmation')
            instance.discount = validated_data.get('discount')
            instance.start_day = validated_data.get('start_day')
            instance.end_day = validated_data.get('end_day')
            if (instance.start_day <= datetime.date.today() <= instance.end_day) and \
                    validated_data.get('discount_confirmation') is True:
                instance.price_before_discount = instance.price
                instance.price = (100 - discount) * int(instance.price) // 100
            instance.save()

        return instance


class CourseCreateSerializer(serializers.ModelSerializer):
    queryset = Category.objects.all()
    category = serializers.PrimaryKeyRelatedField(queryset=queryset,
                                                  read_only=False,
                                                  many=False)

    class Meta:
        model = Course
        fields = ['id', 'title', 'content', 'category', 'price']


# Сериализатор для страницы со списком курсов без возможности их создавать
class CourseListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'content', 'category', 'price',
                  'discount_confirmation', 'discount', 'start_day', 'end_day']



User = get_user_model()


class CourseTitleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ['id', 'title']
# User Serializer


class UserSerializer(serializers.ModelSerializer):
    user_courses = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_superuser', 'user_courses')

    def get_user_courses(self, obj):
        # user_courses = UserCourse.objects.filter(user_id=obj.id)
        # return UserCourseSerializer(user_courses, many=True).data

        user_courses = UserCourse.objects.filter(user_id=obj.id)
        user_courses_info = UserCourseSerializer(user_courses, many=True).data
        user_id = obj.id
        course_ids = [item['course_id'] for item in user_courses_info if item['user_id'] == user_id]
        course_list = []
        flat_list = []
        for i in course_ids:
            user_courses = Course.objects.filter(id=i)
            course_info = CourseTitleSerializer(user_courses, many=True).data
            course_list.append(course_info)
            flat_list = [item for sublist in course_list for item in sublist]

        return flat_list


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    user_type = serializers.ChoiceField(choices=('Student', 'Teacher'))
    is_superuser = serializers.BooleanField(default=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'user_type', 'is_superuser',)

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password'],
            is_superuser=validated_data.get('is_superuser', False),

        )
        user.first_name = validated_data.get('first_name', '')
        user.last_name = validated_data.get('last_name', '')

        user.save()

        user_type = validated_data.get('user_type')

        if user_type == 'student':
            # add student-specific fields to user object
            pass
        elif user_type == 'teacher':
            # add teacher-specific fields to user object
            pass

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    data['user'] = user
                else:
                    msg = 'Учетная запись пользователя отключена.'
                    raise serializers.ValidationError(msg)
            else:
                msg = 'невозможно войти в систему с предоставленными учетными данными'
                raise serializers.ValidationError(msg)
        else:
            msg = 'Должно включать "имя пользователя" и "пароль".'
            raise serializers.ValidationError(msg)

        return data


class MaterialSerializer(ModelSerializer):
    class Meta:
        model = Material
        fields = ('id', 'name', 'course_id', 'preview', 'content')


class UserCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCourse
        fields = ('user_id', 'course_id')


class CourseDetailSerializer(serializers.ModelSerializer):
    course_material = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'content', 'course_material']

    def get_course_material(self, obj):
        course_material = Material.objects.filter(course_id=obj.id)
        course_material = MaterialSerializer(course_material, many=True).data
        return course_material