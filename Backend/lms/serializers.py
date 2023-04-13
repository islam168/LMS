from rest_framework import serializers
from .models import Course, Category
import datetime
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model, authenticate


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


class CourseCreateSerializer(serializers.ModelSerializer):
    queryset = Category.objects.all()
    # datasource = DatasourceSerializer(many=False, read_only=False) , will be uncommented below
    category = serializers.PrimaryKeyRelatedField(queryset=queryset,
                                                    read_only=False,
                                                    many=False)
    class Meta:
        model = Course
        fields = ['id', 'title', 'content', 'category', 'price', 'discount_confirmation', 'discount', 'start_day',
                  'end_day']


# Сериализатор для страницы со списком курсов без возможности их создавать
class CourseListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'content', 'category', 'price', 'discount_confirmation', 'discount', 'start_day',
                  'end_day']

    '''
    разобраться с методом ниже (to_representation)
    '''
    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if (str(instance.start_day) < str(datetime.date.today())) and (
                str(instance.end_day) < str(datetime.date.today())):
            representation['discount_confirmation'] = False

        elif (str(instance.start_day) < str(datetime.date.today()) and str(
                instance.end_day) == str(datetime.date.today())) and \
                representation['discount_confirmation'] is True:
            representation['discount_confirmation'] = True

        elif (str(instance.start_day) == str(datetime.date.today()) and str(
                instance.end_day) == str(datetime.date.today())) and \
                representation['discount_confirmation'] is True:
            representation['discount_confirmation'] = True

        else:
            if str(instance.start_day) > str(datetime.date.today()):
                representation['discount_confirmation'] = False

            if str(instance.start_day) >= str(instance.end_day):
                representation['discount_confirmation'] = False

            if str(instance.end_day) == str(datetime.date.today()):
                representation['discount_confirmation'] = False

        if representation['discount_confirmation'] is False:
            representation.pop('discount_confirmation')
            representation.pop('discount')
            representation.pop('start_day')
            representation.pop('end_day')
        else:
            discount = int(instance.discount)
            course_price = (100 - discount) * int(instance.price) // 100
            representation['price'] = course_price

        return representation


User = get_user_model()


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_superuser')


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


from rest_framework.serializers import ModelSerializer
from lms.models import Post


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ('name', 'preview', 'content')