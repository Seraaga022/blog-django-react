# Generated by Django 5.0.2 on 2024-05-01 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_rename_create_at_category_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='backGround_color',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='text_color',
        ),
        migrations.AddField(
            model_name='posttag',
            name='backGround_color',
            field=models.TextField(default='39465e'),
        ),
        migrations.AddField(
            model_name='posttag',
            name='text_color',
            field=models.TextField(default='ffffff'),
        ),
    ]
