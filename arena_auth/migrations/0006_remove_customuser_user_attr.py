# Generated by Django 5.0.6 on 2024-06-25 18:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('arena_auth', '0005_customuser_user_attr'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='user_attr',
        ),
    ]
