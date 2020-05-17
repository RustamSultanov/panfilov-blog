# Generated by Django 2.2.12 on 2020-05-17 14:00

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('mickroservices', '0032_texttemplate_extra_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='texttemplate',
            name='extra_body',
            field=wagtail.core.fields.StreamField([('table', wagtail.core.blocks.RawHTMLBlock())], blank=True),
        ),
    ]
