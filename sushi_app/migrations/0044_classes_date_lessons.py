# Generated by Django 2.2.3 on 2020-05-03 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sushi_app', '0043_auto_20200503_0638'),
    ]

    operations = [
        migrations.AddField(
            model_name='classes',
            name='date_lessons',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата занятия'),
        ),
    ]
