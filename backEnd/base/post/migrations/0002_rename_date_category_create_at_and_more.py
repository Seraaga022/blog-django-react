# Generated by Django 5.0.2 on 2024-04-30 14:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='date',
            new_name='create_at',
        ),
        migrations.RenameField(
            model_name='tag',
            old_name='bg_color',
            new_name='backGround_color',
        ),
        migrations.RenameField(
            model_name='tag',
            old_name='txt_color',
            new_name='text_color',
        ),
        migrations.RemoveField(
            model_name='category',
            name='description',
        ),
        migrations.RemoveField(
            model_name='post',
            name='category',
        ),
        migrations.RemoveField(
            model_name='post',
            name='tag',
        ),
    ]
