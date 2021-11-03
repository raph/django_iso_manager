from django.db import models
from django.utils.translation import gettext as _


class DatastoreType(models.TextChoices):
    PATH = 'PATH'
    SSH = 'SSH'


class AuthType(models.TextChoices):
    PATH = 'USER'
    SSH = 'KEY'

class OsType(models.TextChoices):
    WINDOWS = 'WINDOWS', _('Windows')
    APPLE = 'APPLE', _('Apple')
    LINUX = 'LINUX', _('Linux')
    BSD = 'BSD', _('BSD')
    VMWARE = 'VMWARE', _('VMware')
    STORAGE = 'STORAGE', _('Storage Appliances')
    VIRTUALIZATION = 'VIRTUALIZATION', _('Virtualization Appliances')
    FIREWALL = 'FIREWALL', _('Firewall Appliances')
    FIRMWARE = 'FIRMWARE', _('Firmware and driver utilities')
    RECOVERY = 'RECOVERY', _('Recovery Tools')
    OTHER = 'OTHER', _('Other')


class OsArch(models.TextChoices):
    X86 = 'X86', _('x86')
    AMD64 = 'AMD64', _('amd64')
    ARMV8 = 'ARMV8', _('ArmV8')
    DARWIN_ARM64 = 'DARWIN_ARM64', _('darwin_arm64')


class OsLanguage(models.TextChoices):
    ENGLISH = 'ENGLISH', _('English')
    FRENCH = 'FRENCH', _('French')

class VersionScheme(models.TextChoices):
    SEMVER = 'SEM', 'SemVer'
    CALVER = 'CAL', 'CalVer'
