# Generated by Django 4.1.7 on 2023-02-18 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0009_course_end_time_course_start_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='price',
            field=models.DecimalField(decimal_places=2, default=100000, max_digits=9),
        ),
    ]