from django.contrib import admin

# Register your models here.

from .models import LocalCatalog, RemoteCatalog, LibraryItem, LibraryTarget, Datastore

@admin.register(LocalCatalog, RemoteCatalog, LibraryItem, LibraryTarget, Datastore)
class DefaultAdmin(admin.ModelAdmin):
    pass