# Generated by Django 2.2.3 on 2020-04-08 18:27

from django.db import migrations
import recurrence.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sushi_app', '0041_classes_is_not_attended'),
    ]

    operations = [
        migrations.AddField(
            model_name='classes',
            name='recurrences',
            field=recurrence.fields.RecurrenceField(blank=True),
        ),
    ]