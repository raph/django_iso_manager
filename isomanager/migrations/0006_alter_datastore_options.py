# Generated by Django 3.2.8 on 2021-10-20 03:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('isomanager', '0005_auto_20211020_0311'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='datastore',
            options={'ordering': ['-last_scan'], 'verbose_name': 'Datastore', 'verbose_name_plural': 'Datastores'},
        ),
    ]
