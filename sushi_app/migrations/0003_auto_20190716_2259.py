# Generated by Django 2.2.2 on 2019-07-16 19:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailusers', '0009_userprofile_verbose_name_plural'),
        ('sushi_app', '0002_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_manager',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='is_partner',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='manager', to='wagtailusers.UserProfile'),
        ),
    ]
