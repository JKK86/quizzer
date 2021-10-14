# Generated by Django 3.2.8 on 2021-10-14 12:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quiz_app', '0003_alter_questionorder_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='quizzes_created', to=settings.AUTH_USER_MODEL),
        ),
    ]
