# Generated by Django 3.1.4 on 2021-01-15 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_stuff', '0026_notification_object_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notificationlist',
            name='has_new',
        ),
        migrations.AddField(
            model_name='notificationlist',
            name='number_of_new',
            field=models.IntegerField(default=0),
        ),
    ]
