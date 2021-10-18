from django.db import models

import recurrence.fields

# Create your models here.

# The local ISO Catalog model
class LocalCatalog(models.Model):
    library_item = models.ForeignKey(LibraryItem)
	download_urls = models.JSONField
	last_update = models.DateTimeField('last update')
    class VersionScheme(models.TextChoices):
    	SEMVER = 'SEM', _('SemVer')
        CALVER = 'CAL', _('CalVer')   
    versionscheme = models.CharField(
        max_length=3,
        choices=OsType.choices,
        default=OsType.SemVer,
        )
    version = models.CharField(max_length=255)
    maintainer = models.CharField(max_length=255)
    sha256sum = models.CharField(max_length=64)
    class OsType(models.TextChoices):
        WINDOWS = 'WIN', _('Windows')
        MACOS = 'MAC', _('macOS')             
        LINUX = 'LNX', _('Linux')
        BSD = 'BSD', _('BSD')
        VMWARE = 'VMW', _('VMware')
        STORAGE = 'STR', _('Storage Appliances')
        VIRTUALIZATION = 'VIR', _('Virtualization Appliances')
        FIREWALL = 'FIR', _('Firewall Appliances')
        FIRMWARE = 'FIR', _('Firmware and driver utilities')
        RECOVERY = 'REC', _('Recovery Tools')
        OTHER = 'ETC', _('Other')
    ostype = models.CharField(
        max_length=3,
        choices=OsType.choices,
        default=OsType.Linux
        )
    detachedfromhead = models.BooleanField()

# The public catalog of ISO images

class RawCatalog(models.Model):
    json_catalog = models.JSONField
    version = models.Charfield(max_length=32)
    remote_location = models.Charfield(max_length=255)
    auto_update = models.BooleanField(initial=True)

# The library of ISO images detected locally (updated by folder scan)

class LibraryItem(models.Model):
    localname = models.CharField
    datastore = models.ForeignKey(Datastore)
    sha256sum = models.CharField(max_length=64)
    targeted_by = models.ForeignKey(LibraryTarget, on_delete=models.CASCADE)

# The library of items to be downloaded and updated

class LibraryTarget(models.Model):
    name = models.CharField(max_length=255)
    desired_version = models.CharField(max_length=32)
    update_check_frequency = recurrence.fields.RecurrenceField()

# The datastore class

class Datastore(models.Model):
    class DatastoreType(models.TextChoices):
        PATH = 'PATH'
        NFS = 'NFS'
        CIFS = 'CIFS'
        SFTP = 'SFTP'
        FTP = 'FTP'
    datastoretype = models.Charfield(
        max_length=4,
        choices = DatastoreType.choices,
        default = DatastoreType.Localpath
        )
    readonly = models.BooleanField()
	last_update = models.DateTimeField('last update')

