# Generated by Django 5.0.2 on 2024-04-29 11:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('post', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Draft',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('content', models.TextField()),
                ('img', models.TextField(default='empty')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
        ),
        migrations.CreateModel(
            name='DraftCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='post.category')),
                ('draft', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='draft.draft')),
            ],
        ),
        migrations.CreateModel(
            name='DraftTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('draft', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='draft.draft')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='post.tag')),
            ],
        ),
    ]