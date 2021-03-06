# Generated by Django 2.0.2 on 2018-11-26 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb_master', '0005_auto_20181126_1711'),
    ]

    operations = [
        migrations.AddField(
            model_name='networkdevice',
            name='auth_key',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='Snmp_authkey'),
        ),
        migrations.AddField(
            model_name='networkdevice',
            name='priv_key',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='snmp_privkey'),
        ),
        migrations.AddField(
            model_name='networkdevice',
            name='snmp_community',
            field=models.CharField(default='public', max_length=128, verbose_name='Snmp团体名'),
        ),
        migrations.AddField(
            model_name='networkdevice',
            name='snmp_version',
            field=models.CharField(choices=[('1', '1'), ('2', '2c'), ('3', '3')], default='2', max_length=25, verbose_name='snmp版本'),
        ),
        migrations.AddField(
            model_name='server',
            name='auth_key',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='Snmp_authkey'),
        ),
        migrations.AddField(
            model_name='server',
            name='priv_key',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='snmp_privkey'),
        ),
        migrations.AddField(
            model_name='server',
            name='snmp_community',
            field=models.CharField(default='public', max_length=128, verbose_name='Snmp团体名'),
        ),
        migrations.AddField(
            model_name='server',
            name='snmp_version',
            field=models.CharField(choices=[('1', '1'), ('2', '2c'), ('3', '3')], default='2', max_length=25, verbose_name='snmp版本'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='device_type_id',
            field=models.IntegerField(choices=[(1, '服务器'), (2, '交换机'), (3, '防火墙'), (4, '路由器'), (5, 'IDS'), (6, 'IPS'), (7, 'WAF'), (8, '负载均衡')], default=1),
        ),
    ]
