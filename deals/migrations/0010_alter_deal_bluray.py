# Generated by Django 4.0.3 on 2022-04-02 11:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blurays', '0012_alter_bluray_request'),
        ('deals', '0009_alter_deal_bluray'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deal',
            name='bluray',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='deal_bluray', to='blurays.bluray'),
        ),
    ]
