# Generated by Django 5.0.2 on 2024-05-01 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.TextField(default='customer'),
        ),
    ]