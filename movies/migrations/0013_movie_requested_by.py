# Generated by Django 4.0.3 on 2022-04-03 11:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movies', '0012_alter_movie_imdb_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='requested_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='movie_requested_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
