# Generated by Django 2.0.2 on 2018-11-28 01:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb_master', '0007_auto_20181127_1809'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cpu',
            old_name='capacity',
            new_name='percent',
        ),
        migrations.RenameField(
            model_name='nic',
            old_name='hwaddr',
            new_name='hwAddr',
        ),
    ]
