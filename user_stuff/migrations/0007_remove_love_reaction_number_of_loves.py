# Generated by Django 3.1.4 on 2021-01-07 18:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_stuff', '0006_love_reaction'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='love_reaction',
            name='number_of_loves',
        ),
    ]