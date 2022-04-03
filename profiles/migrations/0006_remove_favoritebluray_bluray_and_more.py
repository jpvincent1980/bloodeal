# Generated by Django 4.0.3 on 2022-04-02 10:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blurays', '0012_alter_bluray_request'),
        ('profiles', '0005_alter_favoritebluray_blu_ray'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favoritebluray',
            name='blu_ray',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_bluray', to='blurays.bluray'),
        ),
    ]
