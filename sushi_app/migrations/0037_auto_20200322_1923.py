# Generated by Django 2.2.3 on 2020-03-22 16:23

import django.contrib.postgres.fields.ranges
import django.contrib.postgres.indexes
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sushi_app', '0036_requests_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='Classes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration', django.contrib.postgres.fields.ranges.DateTimeRangeField(db_index=True, unique=True, verbose_name='Время занятия')),
                ('type_classes', models.SmallIntegerField(choices=[(0, 'Индивидуальная тренировка'), (1, 'Индивидуальная тренировка 1+1')], default=0, verbose_name='Тип занятия')),
                ('is_busy', models.BooleanField(default=False, verbose_name='Занято')),
                ('is_attended', models.BooleanField(default=False, verbose_name='Посещено')),
                ('is_paid', models.BooleanField(default=False, verbose_name='Оплачено')),
                ('date_paid', models.DateField(blank=True, null=True, verbose_name='Дата оплаты')),
                ('check_link', models.URLField(blank=True, null=True, verbose_name='Ссылка на чек')),
                ('cost', models.IntegerField(default=2500, verbose_name='Стоимость')),
            ],
            options={
                'verbose_name': 'Занятия',
            },
        ),
        migrations.AddIndex(
            model_name='classes',
            index=django.contrib.postgres.indexes.GistIndex(fields=['duration'], name='sushi_app_c_duratio_ba5520_gist'),
        ),
    ]
