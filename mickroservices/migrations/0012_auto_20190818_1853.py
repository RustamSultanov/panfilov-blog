# Generated by Django 2.2.3 on 2019-08-18 15:53

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('mickroservices', '0011_documentsushi'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ideamodel',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='ideamodel',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, verbose_name='Номер телефона'),
        ),
        migrations.AlterField(
            model_name='questionmodel',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='questionmodel',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, verbose_name='Номер телефона'),
        ),
    ]
