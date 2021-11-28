# Generated by Django 3.1.4 on 2021-01-10 05:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_stuff', '0019_comment_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='is_loved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='comment',
            name='number_of_comment',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='Love_Reaction_On_Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='user_stuff.comment')),
                ('user', models.ManyToManyField(related_name='lovingUserofcomment', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
