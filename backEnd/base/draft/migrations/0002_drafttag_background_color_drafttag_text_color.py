# Generated by Django 5.0.2 on 2024-05-01 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('draft', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='drafttag',
            name='backGround_color',
            field=models.TextField(default='39465e'),
        ),
        migrations.AddField(
            model_name='drafttag',
            name='text_color',
            field=models.TextField(default='ffffff'),
        ),
    ]
