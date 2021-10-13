# Generated by Django 3.2.8 on 2021-10-13 12:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='category',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='quiz_app.category'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quiz',
            name='slug',
            field=models.SlugField(blank=True, max_length=128),
        ),
    ]
