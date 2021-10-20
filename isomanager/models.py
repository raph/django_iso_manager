import recurrence.fields
from django.db import models
from django.utils.translation import gettext as _

from isomanager.choices import DatastoreType, OsType, OsArch, OsLanguage, VersionScheme, AuthType


class Datastore(models.Model):
    """
    The datastore class used to list monitored folder
    """
    datastore_type = models.CharField(_('Datastore'), help_text=_('Datastore type, local path and SSH are supported'),
                                      max_length=4, choices=DatastoreType.choices, default=DatastoreType.PATH)
    location = models.CharField(_('Location'), help_text=_('The the location of the datastore'),max_length=255)
    auth_type = models.CharField(_('Auth Type'), help_text=_('Authentication type, username or key, only used for SSH'),
                                      max_length=4, choices=AuthType.choices, blank=True, null=True)
    username = models.CharField(_('Username'), help_text=_('SSH Username'),max_length=64, blank=True, null=True)
    password = models.CharField(_('Password'), help_text=_('SSH Password'),max_length=64, blank=True, null=True)
    readonly = models.BooleanField(_('Read-only'),
                                   help_text=_('True if the iso manager does not have write permission'))
    last_scan = models.DateTimeField(_('Last scan'), help_text=_('Time this datastore was last scanned'),
                                     blank=True, null=True)

    def __str__(self):
        return "{0} - {1}".format(self.datastore_type, self.location)

    class Meta:
        verbose_name = _('Datastore')
        verbose_name_plural = _('Datastores')
        ordering = ['-last_scan']


class RemoteCatalog(models.Model):
    """
    The public catalog of ISO images
    """
    catalog_name = models.CharField(_('Catalog name'), help_text=_('The name of the catalog'), max_length=32)
    json_catalog = models.JSONField(_('JSON catalog'), help_text=_('The JSON model as downloaded from the upstream'))
    version = models.CharField(_('Version'), help_text=_('Version of the JSON catalog'), max_length=32)
    remote_url = models.CharField(_('Remote URL'), help_text=_('Remote URL to update the JSON model'), max_length=255)
    auto_update = models.BooleanField(_('Auto Update'), help_text=_('Auto update the JSON catalog'), default=True)
    priority = models.CharField(_('Priority'), help_text=_(
        'Catalog items with higher priority will override those with lower priority'), max_length=3, unique=True)

    def __str__(self):
        return "{0}".format(self.catalog_name)

    class Meta:
        verbose_name = _('Catalog')
        verbose_name_plural = _('Catalogs')
        ordering = ['-priority']


class OsEdition(models.Model):
    os_edition_name = models.CharField(_('OS Edition'), help_text=_('The edition of the OS'), max_length=32,
                                       unique=True)
    def __str__(self):
        return "{0}".format(self.os_edition_name)

    class Meta:
        verbose_name = _('OS Edition Name')
        verbose_name_plural = _('OS Edition Names')


class LocalCatalog(models.Model):
    """
    The local image Catalog model
    """
    library_item = models.ForeignKey(LibraryItem, on_delete=models.DO_NOTHING)
    download_urls = models.JSONField,
    last_update = models.DateTimeField(_('Last Update'), help_text=_('Time last scanned'))
    version_scheme = models.CharField(_('Version Scheme'), help_text=_('The version scheme being used'), max_length=3,
                                      choices=VersionScheme.choices, default=VersionScheme.SEMVER)
    version_number = models.CharField(_('Version Number'), help_text=_('The version number of the item'), max_length=255)
    maintainer = models.CharField(_('Maintainer'), help_text=_('The version number of the item'), max_length=255)
    sha256sum = models.CharField(_('SHA256 Checksum'), help_text=_('The SHA256 checksum of the item'), max_length=64,
                                 unique=True)
    os_type = models.CharField(_('OS Type'), help_text=_('The type of image'), max_length=16,
                               choices=OsType.choices, default=OsType.LINUX)
    os_edition = models.ForeignKey(OsEdition, _('OS Edition'), help_text=_('The edition of the OS'), max_length=32)
    os_language = models.CharField(_('Language'), help_text=_('The language of the item in the catalog'),
                                   choices=OsLanguage.choices)
    os_arch = models.CharField(_('OS Architecture'), help_text=_('The architecture of the OS'), max_length=16,
                               choices=OsArch.choices, default=OsArch.AMD64)
    detached_from_head = models.BooleanField(_('Detached from head'),
                                             help_text=_('True if the item has been manually edited'))
    release_date = models.DateTimeField(_('Release date'), help_text=_('The release date of this version'))

    def __str__(self):
        return "{0} {1}".format(self.os_edition, self.version_number)

    class Meta:
        verbose_name = _('Catalog Item')
        verbose_name_plural = _('Catalog Items')
        ordering = ['-release_date']


class LibraryTarget(models.Model):
    """
    The list of items to be downloaded and updated
    """
    name = models.CharField(max_length=255)
    desired_version = models.CharField(max_length=32)
    update_check_frequency = recurrence.fields.RecurrenceField()
    catalog_item = models.ForeignKey(_('Catalog Item'), help_text=_('The catalog item linked to this target'),
                                     LocalCatalog, on_delete=models.RESTRICT)

class ManagedItem(models.Model):
    """"
    scans :model:`isomanager.Datastore`.
    The library of ISO images detected locally (updated by folder scan)
    """
    full_path = models.CharField(max_length=255)
    datastore = models.ForeignKey(Datastore, on_delete=models.CASCADE)
    sha256sum = models.CharField(max_length=64)
    targeted_by = models.ForeignKey(_('Targeted by'), help_text=_('The target '), LibraryTarget,
                                    on_delete=models.DO_NOTHING)

