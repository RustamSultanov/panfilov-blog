# Generated by Django 2.2.3 on 2019-09-15 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sushi_app', '0032_auto_20190915_2343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messeges',
            name='file',
            field=models.FileField(blank=True, upload_to=''),
        ),
    ]
