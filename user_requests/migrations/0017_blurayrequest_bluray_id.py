# Generated by Django 4.0.3 on 2022-04-04 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_requests', '0016_alter_movierequest_title_vf'),
    ]

    operations = [
        migrations.AddField(
            model_name='blurayrequest',
            name='bluray_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
