# Generated by Django 2.0.2 on 2018-02-22 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20180220_1438'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(default='', max_length=60, unique=True),
        ),
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(default='', max_length=60, unique=True),
        ),
        migrations.AddField(
            model_name='pseudo',
            name='slug',
            field=models.SlugField(default='', max_length=60, unique=True),
        ),
        migrations.AddField(
            model_name='tag',
            name='slug',
            field=models.SlugField(default='', max_length=60, unique=True),
        ),
    ]