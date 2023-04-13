# Generated by Django 4.1.7 on 2023-04-12 07:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0018_alter_course_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='end_day',
            field=models.DateField(default=datetime.date(2023, 4, 13), verbose_name='День окончания скидок: '),
        ),
        migrations.AlterField(
            model_name='course',
            name='start_day',
            field=models.DateField(default=datetime.date(2023, 4, 12), verbose_name='День старта скидок: '),
        ),
    ]
