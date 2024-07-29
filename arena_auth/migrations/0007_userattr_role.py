# Generated by Django 5.0.6 on 2024-07-29 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arena_auth', '0006_remove_customuser_user_attr'),
    ]

    operations = [
        migrations.AddField(
            model_name='userattr',
            name='role',
            field=models.CharField(choices=[('Manager', 'Manager'), ('Supervisor', 'Supervisor'), ('Creator', 'Creator'), ('Member', 'Member')], default='Member', max_length=10),
        ),
    ]
