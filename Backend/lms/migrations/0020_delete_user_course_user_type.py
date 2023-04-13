# Generated by Django 4.1.5 on 2023-03-27 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0019_user_alter_course_end_day_alter_course_start_day'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
        migrations.AddField(
            model_name='course',
            name='user_type',
            field=models.CharField(choices=[('Student', 'Student'), ('Teacher', 'Teacher')], default='Student', max_length=10),
        ),
    ]
