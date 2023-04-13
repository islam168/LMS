# Generated by Django 4.1.7 on 2023-03-02 16:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0014_alter_course_end_day_alter_course_start_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='end_day',
            field=models.DateField(default=datetime.date(2023, 3, 3), verbose_name='День окончания скидок: '),
        ),
        migrations.AlterField(
            model_name='course',
            name='start_day',
            field=models.DateField(default=datetime.date(2023, 3, 2), verbose_name='День старта скидок: '),
        ),
    ]
