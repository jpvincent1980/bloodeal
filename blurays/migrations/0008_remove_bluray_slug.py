# Generated by Django 4.0.3 on 2022-03-27 17:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blurays', '0007_alter_bluray_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bluray',
            name='slug',
        ),
    ]
