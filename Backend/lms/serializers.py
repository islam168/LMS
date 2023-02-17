from rest_framework import serializers
from .models import Course, Category


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'

# Сериализатор для страницы со списком курсов с возможности их создавать
class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ['title', 'content', 'category']

# Сериализатор для страницы со списком курсов без возможности их создавать
class CourseListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False, read_only=True)

    class Meta:
        model = Course
        fields = ['title', 'content', 'category']
