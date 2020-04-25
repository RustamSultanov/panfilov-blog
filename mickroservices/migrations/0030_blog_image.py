# Generated by Django 2.2.3 on 2020-04-25 17:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0001_squashed_0021'),
        ('mickroservices', '0029_auto_20200308_0119'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image', verbose_name='Фоновая картинка'),
        ),
    ]
