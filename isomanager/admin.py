from django.contrib import admin

from .models import CatalogItem, Datastore, ManagedItem, OsEdition, RemoteCatalog, UpdateTarget


# Register your models here.

@admin.register(CatalogItem, RemoteCatalog, ManagedItem, UpdateTarget, Datastore, OsEdition)
class DefaultAdmin(admin.ModelAdmin):
    pass
