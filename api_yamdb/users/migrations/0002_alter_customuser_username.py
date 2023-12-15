# Generated by Django 3.2 on 2023-12-15 15:57

import django.contrib.auth.validators
from django.db import migrations, models
import users.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(help_text='Имя пользователя', max_length=150, unique=True, validators=[users.validators.validate_username, django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='Username'),
        ),
    ]
