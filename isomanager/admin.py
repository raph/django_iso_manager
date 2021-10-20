from django.contrib import admin

# Register your models here.

from .models import LocalCatalog, RemoteCatalog, ManagedItem, LibraryTarget, Datastore

@admin.register(LocalCatalog, RemoteCatalog, ManagedItem, LibraryTarget, Datastore)
class DefaultAdmin(admin.ModelAdmin):
    pass