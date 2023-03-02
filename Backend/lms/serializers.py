from rest_framework import serializers
from .models import Course, Category
import datetime
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model, authenticate


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False, read_only=True)

    class Meta:
        model = Course
        fields = ['title', 'content', 'category', 'price', 'discount_confirmation', 'discount', 'start_day',
                  'end_day']

# Сериализатор для страницы со списком курсов без возможности их создавать
class CourseListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False, read_only=True)

    class Meta:
        model = Course
        fields = ['title', 'content', 'category', 'price', 'discount_confirmation', 'discount', 'start_day',
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
        fields = ('id', 'username', 'email', 'is_superuser')


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password', 'is_superuser')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            password=validated_data.get('password'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
        )
        return user

    def create(self, validated_data):
        is_superuser = validated_data.pop('is_superuser')
        user = User.objects.create(**validated_data)
        if is_superuser:
            user.is_superuser = True
            user.save()
        return user

    def update(self, instance, validated_data):
        is_superuser = validated_data.pop('is_superuser', instance.is_superuser)
        user = super().update(instance, validated_data)
        user.is_superuser = is_superuser
        user.save()
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
                    raise serializers.ValidationError
            else:
                raise serializers.ValidationError
        else:
            raise serializers.ValidationError

        return data






