# Generated by Django 2.2.3 on 2020-05-03 03:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('joyous', '0015_auto_20190409_0645'),
        ('sushi_app', '0042_classes_recurrences'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classes',
            name='recurrences',
        ),
        migrations.AddField(
            model_name='classes',
            name='recurrences_event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='classes', to='joyous.RecurringEventPage', verbose_name='Событие'),
        ),
    ]