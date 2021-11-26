# Generated by Django 3.2.8 on 2021-11-15 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('isomanager', '0002_auto_20211112_1231'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='catalogitem',
            name='detached_from_head',
        ),
        migrations.RemoveField(
            model_name='catalogitem',
            name='maintainer',
        ),
        migrations.RemoveField(
            model_name='catalogitem',
            name='os_edition',
        ),
        migrations.AddField(
            model_name='catalogitem',
            name='author',
            field=models.CharField(default='aaa', help_text='The author of the OS', max_length=32, verbose_name='OS Author'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='catalogitem',
            name='contributors',
            field=models.CharField(default='aaa', help_text='Contributors', max_length=255, verbose_name='Contributors'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='catalogitem',
            name='description',
            field=models.CharField(default='aaa', help_text='Item description', max_length=100, verbose_name='Description'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='catalogitem',
            name='documentation_url',
            field=models.CharField(default='uuu', help_text='URL of the OS documentation', max_length=255, verbose_name='OS Documentation URL'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='catalogitem',
            name='homepage_url',
            field=models.CharField(default={'url': 'google.com'}, help_text='URL of the OS homepage', max_length=255, verbose_name='Homepage URL'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='catalogitem',
            name='keywords',
            field=models.CharField(default='aaa', help_text='Related keywords', max_length=255, verbose_name='Keywords'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='catalogitem',
            name='language',
            field=models.CharField(default='aa', help_text='The language of the OS', max_length=32, verbose_name='OS Language'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='catalogitem',
            name='original_filename',
            field=models.CharField(default='aaaa', help_text='The original filename of the item', max_length=255, verbose_name='Filename'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='catalogitem',
            name='os_arch',
            field=models.CharField(default='aaaa', help_text='The Architecture of the OS', max_length=32, verbose_name='OS Architecture'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='catalogitem',
            name='os_edition_name',
            field=models.CharField(default='aaaa', help_text='Name of the the edition of the OS', max_length=32, verbose_name='OS Edition Name'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='catalogitem',
            name='os_type',
            field=models.CharField(default='aaa', help_text='The type of the OS', max_length=32, verbose_name='OS Type'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='catalogitem',
            name='private',
            field=models.BooleanField(default=False, help_text='Private', verbose_name='Private'),
        ),
        migrations.AddField(
            model_name='catalogitem',
            name='sha256sumgpg',
            field=models.TextField(default='aaa', help_text='GPG key of the checksum', verbose_name='GPG key'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='catalogitem',
            name='version',
            field=models.CharField(default='aaa', help_text='The version of the OS', max_length=32, verbose_name='OS Version'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='catalogitem',
            name='download_urls',
            field=models.JSONField(help_text='The JSON object containing URLs to download the OS', verbose_name='URLs to download OS'),
        ),
        migrations.AlterField(
            model_name='catalogitem',
            name='last_update',
            field=models.DateTimeField(auto_now=True, help_text='Time last scanned', verbose_name='Last Update'),
        ),
        migrations.AlterField(
            model_name='catalogitem',
            name='sha256sum',
            field=models.CharField(help_text='SHA256 Checksum for this file', max_length=255, verbose_name='SHA256 Checksum'),
        ),
        migrations.AlterField(
            model_name='catalogitem',
            name='version_scheme',
            field=models.CharField(help_text='Version scheme of the OS', max_length=32, verbose_name='OS Version Scheme'),
        ),
    ]
