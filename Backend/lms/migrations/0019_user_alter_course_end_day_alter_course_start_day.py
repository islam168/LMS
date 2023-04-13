# Generated by Django 4.1.5 on 2023-03-27 06:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0018_alter_course_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_type', models.CharField(choices=[('Student', 'Student'), ('Teacher', 'Teacher')], max_length=10)),
            ],
        ),
        migrations.AlterField(
            model_name='course',
            name='end_day',
            field=models.DateField(default=datetime.date(2023, 3, 28), verbose_name='День окончания скидок: '),
        ),
        migrations.AlterField(
            model_name='course',
            name='start_day',
            field=models.DateField(default=datetime.date(2023, 3, 27), verbose_name='День старта скидок: '),
        ),
    ]
