# Generated by Django 2.0.2 on 2018-11-28 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb_master', '0008_auto_20181128_0948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='disk',
            name='model',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='类型'),
        ),
        migrations.AlterField(
            model_name='memory',
            name='model',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='型号'),
        ),
    ]