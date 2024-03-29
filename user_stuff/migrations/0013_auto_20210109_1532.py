# Generated by Django 3.1.4 on 2021-01-09 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_stuff', '0012_auto_20210109_1519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, upload_to='post_picture'),
        ),
        migrations.AlterField(
            model_name='user_profile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='default.jpg', upload_to='profile_picture'),
        ),
    ]
