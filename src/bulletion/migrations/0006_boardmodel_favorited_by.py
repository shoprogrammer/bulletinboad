# Generated by Django 5.1.3 on 2024-12-02 01:19

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bulletion', '0005_contact'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='boardmodel',
            name='favorited_by',
            field=models.ManyToManyField(related_name='favorite_boards', through='bulletion.Favorite', to=settings.AUTH_USER_MODEL),
        ),
    ]
