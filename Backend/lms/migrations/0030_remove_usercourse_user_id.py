# Generated by Django 4.1.7 on 2023-04-13 10:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0029_alter_usercourse_course_id_alter_usercourse_user_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usercourse',
            name='user_id',
        ),
    ]