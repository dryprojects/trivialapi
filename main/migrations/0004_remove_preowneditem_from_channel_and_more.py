# Generated by Django 4.0.1 on 2022-01-19 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_remove_preowneditem_related_sources'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='preowneditem',
            name='from_channel',
        ),
        migrations.AlterField(
            model_name='preowneditem',
            name='age_of_building',
            field=models.CharField(max_length=20, verbose_name='建筑年代'),
        ),
    ]
