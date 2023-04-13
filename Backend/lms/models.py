import objects as objects
from django.db import models
import datetime


class Category(models.Model):
    category_name = models.CharField(max_length=50)

    def __str__(self):
        return self.category_name


class Course(models.Model):
    default_date = datetime.date.today()
    title = models.CharField('Название', max_length=100, null=False)
    content = models.TextField('Описание', null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False)
    price = models.IntegerField('Цена кусра: ', null=False)
    discount = models.IntegerField('Скидка: ', default=10)
    discount_confirmation = models.BooleanField('Начать акцию',default=False) # галочка
    start_day = models.DateField('День старта скидок: ', default=default_date)  # По умолчанию начало акции сегодня
    end_day = models.DateField('День окончания скидок: ',
                               default=default_date + datetime.timedelta(days=1))  # По умолчанию конец акции завтра

    def __str__(self):
        return self.title


#-------------------

# class UserProfile(models.Model):
#
#     objects = objects.get(name='user_name')
#     name = models.CharField(max_length=100)
#     courses_taken = models.ManyToManyField('Course', through='CourseEnrollment')
#
#     def __str__(self):
#         return self.name
#
#
#
#
#
# class CourseEnrollment(models.Model):
#     user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return f'{self.user_profile.name} enrolled in {self.course.name}'
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    courses_taken = models.OneToManyField(Course, through='UserCourse')

class UserCourse(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateTimeField(auto_now_add=True)