# Generated by Django 4.0.3 on 2022-03-27 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blurays', '0009_bluray_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='bluray',
            name='amazon_aff_link',
            field=models.URLField(blank=True),
        ),
    ]
