# Generated by Django 4.0.3 on 2022-04-02 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_customuser_pseudo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='pseudo',
            field=models.CharField(blank=True, error_messages={'unique': 'Ce pseudo est déjà pris.'}, max_length=24, null=True, unique=True),
        ),
    ]
