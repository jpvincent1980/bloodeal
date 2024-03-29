# Generated by Django 4.0.3 on 2022-04-04 20:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0013_movie_requested_by'),
        ('people', '0012_people_requested_by'),
        ('user_requests', '0019_rename_bluray_id_blurayrequest_bluray'),
    ]

    operations = [
        migrations.AddField(
            model_name='movierequest',
            name='movie',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='movies.movie'),
        ),
        migrations.AddField(
            model_name='peoplerequest',
            name='people',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='people.people'),
        ),
    ]
