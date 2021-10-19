from django.db import models
from django.utils.translation import gettext as _

import recurrence.fields

# Create your models here.

# The datastore class used to list monitored folder

class Datastore(models.Model):
    class DatastoreType(models.TextChoices):
        PATH = 'PATH'
        NFS = 'NFS'
        CIFS = 'CIFS'
        SFTP = 'SFTP'
        FTP = 'FTP'
    datastoretype = models.CharField(
        max_length=4,
        choices = DatastoreType.choices,
        default = DatastoreType.PATH
        )
    readonly = models.BooleanField()
    last_scan = models.DateTimeField('last scan')

# The library of items to be downloaded and updated

class LibraryTarget(models.Model):
    name = models.CharField(max_length=255)
    desired_version = models.CharField(max_length=32)
    update_check_frequency = recurrence.fields.RecurrenceField()

# The library of ISO images detected locally (updated by folder scan)

class LibraryItem(models.Model):
    localname = models.CharField(max_length=255)
    datastore = models.ForeignKey(Datastore, on_delete=models.CASCADE)
    sha256sum = models.CharField(max_length=64)
    targeted_by = models.ForeignKey(LibraryTarget, on_delete=models.DO_NOTHING)

# The local ISO Catalog model
class LocalCatalog(models.Model):
    library_item = models.ForeignKey(LibraryItem, on_delete=models.DO_NOTHING)
    download_urls = models.JSONField,
    last_update = models.DateTimeField('last update')
    class VersionScheme(models.TextChoices):
        SEMVER = 'SEM', ('SemVer')
        CALVER = 'CAL', ('CalVer')   
    versionscheme = models.CharField(
        max_length=3,
        choices=VersionScheme.choices,
        default=VersionScheme.SEMVER,
        )
    version = models.CharField(max_length=255)
    maintainer = models.CharField(max_length=255)
    sha256sum = models.CharField(max_length=64, unique=True)
    class OsType(models.TextChoices):
        WINDOWS = 'WINDOWS', _('Windows')
        MACOS = 'MACOS', _('macOS')             
        LINUX = 'LINUX', _('Linux')
        BSD = 'BSD', _('BSD')
        VMWARE = 'VMWARE', _('VMware')
        STORAGE = 'STORAGE', _('Storage Appliances')
        VIRTUALIZATION = 'VIRTUALIZATION', _('Virtualization Appliances')
        FIREWALL = 'FIREWALL', _('Firewall Appliances')
        FIRMWARE = 'FIRMWARE', _('Firmware and driver utilities')
        RECOVERY = 'RECOVERY', _('Recovery Tools')
        OTHER = 'OTHER', _('Other')
    ostype = models.CharField(
        max_length=16,
        choices=OsType.choices,
        default=OsType.LINUX,
        )
    detachedfromhead = models.BooleanField()

# The public catalog of ISO images

class RemoteCatalog(models.Model):
    json_catalog = models.JSONField
    version = models.CharField(max_length=32)
    remote_location = models.CharField(max_length=255)
    auto_update = models.BooleanField(default=True)
    priority = models.CharField(max_length=3, unique=True)
