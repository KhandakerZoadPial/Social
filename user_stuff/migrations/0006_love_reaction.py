# Generated by Django 3.1.4 on 2021-01-07 17:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_stuff', '0005_auto_20210107_1144'),
    ]

    operations = [
        migrations.CreateModel(
            name='Love_Reaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_loves', models.IntegerField(default=0)),
                ('post', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='user_stuff.post')),
                ('user', models.ManyToManyField(related_name='lovingUser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
