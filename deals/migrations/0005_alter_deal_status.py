# Generated by Django 4.0.3 on 2022-03-29 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deals', '0004_deal_end_date_deal_start_date_alter_deal_amazon_link_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deal',
            name='status',
            field=models.CharField(blank=True, choices=[('1', 'Actif'), ('2', 'Expiré'), ('3', 'Indéterminé')], default='3', max_length=56, null=True),
        ),
    ]
