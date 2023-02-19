from rest_framework import serializers
from .models import Course, Category
import datetime


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


# Сериализатор для страницы со списком курсов с возможности их создавать
class CourseSerializer(serializers.ModelSerializer):

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
            course_price = int(instance.price) * (1-(discount/100))
            representation['price'] = course_price

        return representation
