# Generated by Django 2.0.5 on 2018-06-14 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0021_auto_20180608_1113'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]