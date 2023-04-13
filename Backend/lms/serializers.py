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
        fields = ['id', 'title', 'content', 'category', 'price', 'discount_confirmation','discount', 'start_day',
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

    # course_price = (int(instance.price) * 100) - (100 - discount)

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #
    #     if self.context['request'].method == 'PUT' and instance.discount_confirmation and \
    #             instance.start_day <= datetime.date.today() <= instance.end_day:
    #         discount = int(instance.discount)
    #         course_price = (100 - discount) * int(instance.price) // 100
    #         instance.price = course_price
    #         instance.save()
    #     elif instance.discount_confirmation == False:
    #         discount = int(instance.discount)
    #         course_price = (int(instance.price) * 100) - (100 - discount)
    #         instance.price = course_price
    #         instance.save()
    #
    #     return representation


class CourseCreateSerializer(serializers.ModelSerializer):
    queryset = Category.objects.all()
    # datasource = DatasourceSerializer(many=False, read_only=False) , will be uncommented below
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
        fields = ['id', 'title', 'content', 'category', 'price', 'discount_confirmation', 'discount', 'start_day',
                  'end_day']

    # def update_discount(self, instance):
    #     discount = int(instance.discount)
    #     if (instance.start_day > datetime.date.today() or datetime.date.today() > instance.end_day) \
    #             and instance.discount_confirmation:
    #         instance.price = (int(instance.price) * 100) - (100 - discount)
    #         instance.discount_confirmation = False
    #         instance.save()
    #
    # def to_representation(self, instance):
    #     self.update_discount(instance)
    #     return super().to_representation(instance)


User = get_user_model()


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_superuser')


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
                    msg = 'Учетная запись пользователя отключена.'
                    raise serializers.ValidationError(msg)
            else:
                msg = 'Невозможно войти в систему с предоставленными учетными данными'
                raise serializers.ValidationError(msg)
        else:
            msg = 'Должно включать "имя пользователя" и "пароль".'
            raise serializers.ValidationError(msg)

        return data
        return representation



User = get_user_model()


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email','first_name', 'last_name', 'is_superuser')


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
                    msg = 'Учетная запись пользователя отключена.'
                    raise serializers.ValidationError(msg)
            else:
                msg = 'евозможно войти в систему с предоставленными учетными данными'
                raise serializers.ValidationError(msg)
        else:
            msg = 'Должно включать "имя пользователя" и "пароль".'
            raise serializers.ValidationError(msg)

        return data




