# Generated by Django 4.0.3 on 2022-04-02 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_customuser_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='pseudo',
            field=models.CharField(blank=True, max_length=24, null=True, unique=True),
        ),
    ]
