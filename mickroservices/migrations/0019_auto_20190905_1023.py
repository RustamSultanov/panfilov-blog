# Generated by Django 2.2.3 on 2019-09-05 07:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mickroservices', '0018_auto_20190830_1214'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subjects',
            options={'verbose_name': 'Тематика(папка)', 'verbose_name_plural': 'Тематики(папки)'},
        ),
        migrations.AddField(
            model_name='ideamodel',
            name='recipient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recipient_idea', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ideamodel',
            name='sender',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sender_idea', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='documentsushi',
            name='doc_type',
            field=models.IntegerField(choices=[(0, 'Техкарты'), (1, 'Регламенты'), (2, 'Акции'), (3, 'Перед открытием'), (4, 'Меню'), (5, 'Другие макеты'), (6, 'Видеоролики'), (7, 'Аудиоролики'), (8, 'Личные документы'), (9, 'Личные счета'), (10, 'Обучение')], default=0),
        ),
        migrations.AlterField(
            model_name='subjects',
            name='type',
            field=models.SmallIntegerField(choices=[(0, 'Техкарты'), (1, 'Регламенты'), (2, 'Акции'), (3, 'Перед открытием'), (4, 'Меню'), (5, 'Другие макеты'), (6, 'Видеоролики'), (7, 'Аудиоролики'), (8, 'Личные документы'), (9, 'Личные счета'), (10, 'Обучение')], default=0),
        ),
    ]
