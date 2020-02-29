# Generated by Django 2.2.3 on 2019-07-28 20:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sushi_app', '0016_feedback_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requests',
            name='responsible',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests_responsible', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='task',
            name='responsible',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_responsible', to=settings.AUTH_USER_MODEL),
        ),
    ]
