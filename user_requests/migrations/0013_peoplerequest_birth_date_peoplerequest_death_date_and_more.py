# Generated by Django 4.0.3 on 2022-04-04 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_requests', '0012_alter_blurayrequest_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='peoplerequest',
            name='birth_date',
            field=models.DateField(blank=True, null=True, verbose_name='Date de naissance'),
        ),
        migrations.AddField(
            model_name='peoplerequest',
            name='death_date',
            field=models.DateField(blank=True, null=True, verbose_name='Date de décès'),
        ),
        migrations.AddField(
            model_name='peoplerequest',
            name='first_name',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='peoplerequest',
            name='last_name',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
