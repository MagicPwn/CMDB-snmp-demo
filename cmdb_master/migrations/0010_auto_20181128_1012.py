# Generated by Django 2.0.2 on 2018-11-28 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb_master', '0009_auto_20181128_1009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='disk',
            name='desc',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='介绍'),
        ),
    ]
