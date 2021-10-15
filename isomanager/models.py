from django.db import models

# Create your models here.



# The public catalog of ISO images



# The local ISO Catalog model
class LocalCatalog(models.Model):
	download_urls = models.JSONField
	last_update = models.DateTimeField('last update')
    class VersionScheme(models.TextChoices):
    	SEMVER = 'SEM', _('SemVer')
        CALVER = 'CAL', _('CalVer')   
    versionscheme = models.CharField
        max_length=3,
        choices=OsType.choices,
        default=OsType.SemVer,

    version = models.CharField(max_length=255)
    sha256sum = models.CharField(max_length=64)
    class OsType(models.TextChoices):
        Windows = 'WIN', _('Windows')
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
        default=OsType.Linux,



# The library of ISO images managed locally

class LocalLibrary(models.Model):



# The library of items to be downloaded and updated

class LibraryTarget(models.Model):

