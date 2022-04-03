# Generated by Django 4.0.3 on 2022-04-01 12:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_requests', '0006_alter_blurayrequest_status_alter_movierequest_status_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DealRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amazon_link', models.URLField(verbose_name='Lien Amazon')),
                ('asin', models.CharField(blank=True, max_length=10, null=True)),
                ('price', models.FloatField()),
                ('status', models.CharField(choices=[('1', 'Non traitée'), ('2', 'Acceptée'), ('3', 'Refusée'), ('4', 'Indéterminée')], max_length=56)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deal_user_request', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Ajout - Bon Plan',
                'verbose_name_plural': 'Ajouts - Bons Plans',
            },
        ),
    ]
