# Generated by Django 2.0.5 on 2018-05-15 16:45

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0017_infopage'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('liked_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата и время')),
                ('user_ip', models.GenericIPAddressField(verbose_name='IP посетителя')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Post')),
            ],
        ),
    ]