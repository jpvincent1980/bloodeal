# Generated by Django 4.0.3 on 2022-04-04 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_requests', '0013_peoplerequest_birth_date_peoplerequest_death_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='movierequest',
            name='release_year',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='movierequest',
            name='title_vf',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='movierequest',
            name='title_vo',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
