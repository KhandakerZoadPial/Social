# Generated by Django 3.1.4 on 2021-01-07 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_stuff', '0009_auto_20210108_0120'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_loved',
            field=models.BooleanField(default=True),
        ),
    ]
