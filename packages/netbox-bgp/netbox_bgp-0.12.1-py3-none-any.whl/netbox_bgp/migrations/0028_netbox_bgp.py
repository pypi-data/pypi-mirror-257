# Generated by Django 4.1.9 on 2023-05-16 06:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('netbox_bgp', '0027_netbox_bgp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bgpsession',
            name='device',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='dcim.device'),
        ),
    ]
