# Generated by Django 4.0.3 on 2022-04-02 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blurays', '0013_remove_bluray_request'),
    ]

    operations = [
        migrations.AddField(
            model_name='bluray',
            name='uhd',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
