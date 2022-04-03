# Generated by Django 4.0.3 on 2022-04-01 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_requests', '0005_alter_blurayrequest_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blurayrequest',
            name='status',
            field=models.CharField(choices=[('1', 'Non traitée'), ('2', 'Acceptée'), ('3', 'Refusée'), ('4', 'Indéterminée')], max_length=56),
        ),
        migrations.AlterField(
            model_name='movierequest',
            name='status',
            field=models.CharField(choices=[('1', 'Non traitée'), ('2', 'Acceptée'), ('3', 'Refusée'), ('4', 'Indéterminée')], max_length=56),
        ),
        migrations.AlterField(
            model_name='peoplerequest',
            name='status',
            field=models.CharField(choices=[('1', 'Non traitée'), ('2', 'Acceptée'), ('3', 'Refusée'), ('4', 'Indéterminée')], max_length=56),
        ),
    ]
