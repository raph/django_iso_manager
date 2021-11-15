import json
import logging
from pathlib import Path

import recurrence.fields
from django.db import models
from django.utils.translation import gettext as _

from isomanager.choices import AuthType, DatastoreType, OsArch, OsLanguage, OsType
from isomanager.mixins.model_mixins import TimeMixin
from isomanager.utils import hash

logger = logging.getLogger(__name__)


class Datastore(TimeMixin):
    """
    The datastore class used to list monitored folder
    """
    datastore_type = models.CharField(_('Datastore'), help_text=_('Datastore type, local path and SSH are supported'), max_length=4, choices=DatastoreType.choices, default=DatastoreType.PATH)
    location = models.CharField(_('Location'), help_text=_('The the location of the datastore'), max_length=255)
    auth_type = models.CharField(_('Auth Type'), help_text=_('Authentication type, username or key, only used for SSH'), max_length=4, choices=AuthType.choices, blank=True, null=True)
    username = models.CharField(_('Username'), help_text=_('SSH Username'), max_length=64, blank=True, null=True)
    password = models.CharField(_('Password'), help_text=_('SSH Password'), max_length=64, blank=True, null=True)
    readonly = models.BooleanField(_('Read-only'), help_text=_('True if the iso manager does not have write permission'))
    last_scan = models.DateTimeField(_('Last scan'), help_text=_('Time this datastore was last scanned'), blank=True, null=True)

    # TODO: match to a library item
    def scan(self):
        p = Path(self.location)
        for path in p.glob('**/*.iso'):
            checksum = hash(path)
            catalog_time = None
            print(checksum)
            try:
                catalog_time = CatalogItem.objects.get(sha256sum=checksum)
            except CatalogItem.DoesNotExist:
                logger.error(f'no catalog item were found with checksum: {checksum}')
                pass
            item = ManagedItem.objects.get_or_create(datastore=self, full_path=path, sha256sum=checksum, library_item=catalog_time)
            print(item)

    def __str__(self):
        return "{0} - {1}".format(self.datastore_type, self.location)

    class Meta:
        verbose_name = _('Datastore')
        verbose_name_plural = _('Datastores')
        ordering = ['-last_scan']


class RemoteCatalog(TimeMixin):
    """
    The public catalog of ISO images
    """
    catalog_name = models.CharField(_('Catalog name'), help_text=_('The name of the catalog'), max_length=32)
    json_catalog = models.JSONField(_('JSON catalog'), help_text=_('The JSON model as downloaded from the upstream'))
    version = models.CharField(_('Version'), help_text=_('Version of the JSON catalog'), max_length=32)
    remote_url = models.CharField(_('Remote URL'), help_text=_('Remote URL to update the JSON model'), max_length=255)
    auto_update = models.BooleanField(_('Auto Update'), help_text=_('Auto update the JSON catalog'), default=True)
    priority = models.CharField(_('Priority'), help_text=_('Catalog items with higher priority will override those with lower priority'), max_length=3, unique=True)

    def populate_cat_items(self):
        """
        Populates catalog items from json_catalog, assumes necessary data is present and in correct format
        """
        for image_name, image_data in self.json_catalog['images'].items():
            CatalogItem.objects.create(
                os_type=image_data["os_type"],
                os_edition_name=image_data["os_edition_name"],
                os_arch=image_data["os_arch"],
                description=image_data["description"],
                keywords=image_data["keywords"],
                version_scheme=image_data["version-scheme"],
                version=image_data["version"],
                language=image_data["language"],
                original_filename=image_data["original-filename"],
                sha256sum=image_data["sha256sum"],
                sha256sum_gpg=image_data["sha256sumgpg"],
                private=image_data["private"],
                author=image_data["author"],
                last_update=image_data["lastupdate"],
                release_date=image_data["releasedate"],
                homepage_url=image_data["homepageurl"],
                documentation_url=image_data["documentationurl"],
                contributors=image_data["contributors"],
                download_urls=image_data["download_urls"],
            )

    def __str__(self):
        return "{0}".format(self.catalog_name)

    class Meta:
        verbose_name = _('Catalog')
        verbose_name_plural = _('Catalogs')
        ordering = ['-priority']


class OsEdition(TimeMixin):
    os_edition_type = models.CharField(_('OS Type'), help_text=_('The type of image'), max_length=16, choices=OsType.choices, default=OsType.LINUX)
    os_edition_name = models.CharField(_('OS Edition'), help_text=_('The edition of the OS'), max_length=32)
    os_edition_version = models.CharField(_('Version Number'), help_text=_('The version number of the item'), max_length=32)
    os_edition_arch = models.CharField(_('OS Architecture'), help_text=_('The architecture of the OS'), max_length=16, choices=OsArch.choices, default=OsArch.AMD64)
    os_edition_language = models.CharField(_('Language'), help_text=_('The language of the item in the catalog'), choices=OsLanguage.choices, max_length=64)
    os_edition_version_scheme = models.CharField(_('OS Version Scheme'), help_text=_('The version scheme of the OS'), max_length=32)
    os_edition_description = models.CharField(_('OS description'), help_text=_('Description of the OS'), max_length=32)

    # FIXME: wrong format
    def __str__(self):
        return "{0} - {1} - {2} - {3} - {4}".format(
            self.os_edition_type, self.os_edition_name,
            self.os_edition_version, self.os_edition_arch, self.os_edition_language
        )

    class Meta:
        verbose_name = _('OS Edition')
        verbose_name_plural = _('OS Edition')
        unique_together = ("os_edition_name", "os_edition_version", "os_edition_arch", "os_edition_language")


class CatalogItem(TimeMixin):
    """
    The local image Catalog model
    """

    ### Old model
    # download_urls = models.JSONField(_("Download URLS"), default=list)
    # last_update = models.DateTimeField(_('Last Update'), help_text=_('Time last scanned'))
    # version_scheme = models.CharField(_('Version Scheme'), help_text=_('The version scheme being used'), max_length=3)
    # maintainer = models.CharField(_('Maintainer'), help_text=_('The version number of the item'), max_length=255)
    # sha256sum = models.CharField(_('SHA256 Checksum'), help_text=_('The SHA256 checksum of the item'), max_length=64, unique=True)
    # os_edition = models.ForeignKey('OsEdition', help_text=_('The edition of the OS'), max_length=32, on_delete=models.DO_NOTHING, blank=True, null=True)
    # detached_from_head = models.BooleanField(_('Detached from head'), help_text=_('True if the item has been manually edited'))
    # release_date = models.DateTimeField(_('Release date'), help_text=_('The release date of this version'))

    ### New model
    os_type = models.CharField(_('OS Type'), help_text=_('The type of the OS'), max_length=32)
    os_edition_name = models.CharField(_('OS Edition Name'), help_text=_('Name of the the edition of the OS'), max_length=32)
    os_arch = models.CharField(_('OS Architecture'), help_text=_('The Architecture of the OS'), max_length=32)
    description = models.CharField(_('Description'), help_text=_('Item description'), max_length=100)
    keywords = models.CharField(_('Keywords'), help_text=_('Related keywords'), max_length=255)
    version_scheme = models.CharField(_('OS Version Scheme'), help_text=_('Version scheme of the OS'), max_length=32)
    version = models.CharField(_('OS Version'), help_text=_('The version of the OS'), max_length=32)
    language = models.CharField(_('OS Language'), help_text=_('The language of the OS'), max_length=32)
    original_filename = models.CharField(_('Filename'), help_text=_('The original filename of the item'), max_length=255)
    sha256sum = models.CharField(_('SHA256 Checksum'), help_text=_('SHA256 Checksum for this file'), max_length=255)
    sha256sum_gpg = models.TextField(_('GPG key'), help_text=_('GPG key of the checksum'))
    private = models.BooleanField(_('Private'), help_text=_('Private'), default=False)
    author = models.CharField(_('OS Author'), help_text=_('The author of the OS'), max_length=32)
    last_update = models.DateTimeField(_('Last Update'), help_text=_('Time last scanned'), auto_now=True)
    release_date = models.DateTimeField(_('Release date'), help_text=_('The release date of this version'))
    homepage_url = models.CharField(_('Homepage URL'), help_text=_('URL of the OS homepage'), max_length=255)
    documentation_url = models.CharField(_('OS Documentation URL'), help_text=_('URL of the OS documentation'), max_length=255)
    contributors = models.CharField(_('Contributors'), help_text=_('Contributors'), max_length=255)
    download_urls = models.JSONField(_('URLs to download OS'), help_text=_('The JSON object containing URLs to download the OS'))


    def __str__(self):
        return "{0} {1}".format(self.os_edition_name, self.author)

    class Meta:
        verbose_name = _('Catalog Item')
        verbose_name_plural = _('Catalog Items')
        ordering = ['-release_date']


class UpdateTarget(TimeMixin):
    """
    The list of items to be downloaded and updated
    """
    target_name = models.CharField(_('Auto-Update Name'), help_text=_('The name for this auto-update target'), max_length=64)
    desired_version = models.CharField(_('Desired Version'), help_text=_('The desired target version of this image'), max_length=32)
    update_check_frequency = recurrence.fields.RecurrenceField(_('Update frequency'), help_text=_('How often should this image be updated'))
    catalog_item = models.ForeignKey('CatalogItem', help_text=_('The catalog item linked to this target'), on_delete=models.RESTRICT)
    managed_item = models.ForeignKey('ManagedItem', help_text=_('The items currently satisfying this target'), on_delete=models.DO_NOTHING)

    def __str__(self):
        return "{0}".format(self.target_name)

    class Meta:
        verbose_name = _('Auto-Update Target')
        verbose_name_plural = _('Auto-Update Targets')


class ManagedItem(TimeMixin):
    """"
    scans :model:`isomanager.Datastore`.
    The library of ISO images detected locally (updated by folder scan)
    """
    full_path = models.CharField(max_length=255)
    datastore = models.ForeignKey(Datastore, on_delete=models.CASCADE)
    sha256sum = models.CharField(max_length=64)
    library_item = models.ForeignKey('CatalogItem', on_delete=models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return "({0}) {1}".format(self.sha256sum, self.full_path)

    class Meta:
        verbose_name = _('Managed Item')
        verbose_name_plural = _('Managed Items')
