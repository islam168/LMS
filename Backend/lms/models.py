from django.db import models
import datetime
from django.contrib.auth.models import User


class Category(models.Model):
    category_name = models.CharField(max_length=50)

    def __str__(self):
        return self.category_name


class Course(models.Model):
    default_date = datetime.date.today()
    title = models.CharField('Название', max_length=100, null=False, unique=True)
    content = models.TextField('Описание', null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False)
    price = models.IntegerField('Цена курса: ', null=False)
    price_before_discount = models.IntegerField(default=100000)
    discount = models.IntegerField('Скидка: ', default=10)
    discount_confirmation = models.BooleanField('Начать акцию', default=False)
    start_day = models.DateField('День старта скидок: ', default=default_date)  # По умолчанию начало акции сегодня
    end_day = models.DateField('День окончания скидок: ',
                               default=default_date + datetime.timedelta(days=1))  # По умолчанию конец акции завтра

    def __str__(self):
        return self.title


class Material(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=256)
    preview = models.FileField(upload_to='media/')
    content = models.TextField()

    def __str__(self):
        return self.name


class UserCourse(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f"UserCourse (user_id={self.user_id.id}, course_id={self.course_id.id})"


