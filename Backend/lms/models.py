from django.db import models
import datetime

class Category(models.Model):
    category_name = models.CharField(max_length=50)

    def __str__(self):
        return self.category_name


class Course(models.Model):
    default_date = datetime.date.today()
    title = models.CharField(max_length=100)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    price = models.IntegerField('Цена кусра: ', default=10000)
    discount = models.IntegerField('Скидка: ', default=10)
    discount_confirmation = models.BooleanField('Начать акцию',default=False) # галочка
    start_day = models.DateField('День старта скидок: ', default=default_date)  # По умолчанию начало акции сегодня
    end_day = models.DateField('День окончания скидок: ',
                               default=default_date + datetime.timedelta(days=1))  # По умолчанию конец акции завтра

    def __str__(self):
        return self.title
