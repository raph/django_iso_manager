# Generated by Django 3.2.8 on 2021-11-26 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('isomanager', '0014_alter_remotecatalog_json_catalog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='remotecatalog',
            name='json_catalog',
            field=models.JSONField(blank=True, help_text='The JSON model as downloaded from the upstream', verbose_name='JSON catalog'),
        ),
    ]
