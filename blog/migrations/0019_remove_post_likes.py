# Generated by Django 2.0.5 on 2018-05-18 18:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0018_postlike'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='likes',
        ),
    ]
