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
    user_type = models.CharField(choices=(('Student', 'Student'), ('Teacher', 'Teacher')), max_length=10)

    def __str__(self):
        return self.title


from django.db import models


class Post(models.Model):
    name = models.CharField(max_length=255)
    preview = models.FileField(upload_to='posts')
    content = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
