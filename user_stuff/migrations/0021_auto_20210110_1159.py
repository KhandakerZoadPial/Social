# Generated by Django 3.1.4 on 2021-01-10 05:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_stuff', '0020_auto_20210110_1110'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='number_of_comment',
            new_name='number_of_love',
        ),
    ]