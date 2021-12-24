from import_export.admin import ImportExportModelAdmin

from admin_auto_filters.filters import AutocompleteFilter
from django.contrib import admin, messages
from django.db.models import JSONField
from django.http import HttpResponseRedirect
from django_json_widget.widgets import JSONEditorWidget

# from .forms import CatalogItemForm
from .models import CatalogItem, Datastore, ManagedItem, RemoteCatalog, UpdateTarget



# Register your models here.

@admin.action(description='Scan ISO files')
def scan_action(modeladmin, request, queryset):
    for obj in queryset:
        obj.scan()
    messages.success(request, 'Scanning ISO files is done.')

@admin.register(Datastore)
class DatastoreAdmin(admin.ModelAdmin):
    list_display = ('location', 'datastore_type', 'auth_type', 'readonly', 'last_scan', 'created_time', 'updated_time')
    list_filter = ('datastore_type', 'auth_type', 'readonly')
    date_hierarchy = 'created_time'
    change_form_template = "isomanager/admin/change-form.html"
    actions = [scan_action]

    def response_change(self, request, obj):
        if "scan" in request.POST:
            obj.scan()
            messages.success(request, 'Scanning ISO files is done.')
            return HttpResponseRedirect(".")  # stay on the same detail page

        return super().response_change(request, obj)


@admin.register(RemoteCatalog)
class RemoteCatalog(ImportExportModelAdmin):
    list_display = ('catalog_name', 'version', 'remote_url', 'auto_update', 'priority', 'created_time', 'updated_time')
    list_filter = ('auto_update',)
    date_hierarchy = 'created_time'
    search_fields = ('catalog_name',)
    formfield_overrides = {
        JSONField: {'widget': JSONEditorWidget(mode='tree')},
    }
    change_form_template = "isomanager/admin/remote-cat-populate-items-form.html"

    def response_change(self, request, obj):
        if "populate_cat_items" in request.POST:
            obj.populate_cat_items()
            messages.success(request, 'Populating catalog items from JSON catalog is done.')
            return HttpResponseRedirect(".")  # stay on the same detail page

        return super().response_change(request, obj)


@admin.register(CatalogItem)
class CatalogItemAdmin(ImportExportModelAdmin):
    # form = CatalogItemForm
    list_display = ('os_edition_name', 'sha256sum', 'release_date', 'created_time')
    # list_filter = (OsEditionFilter,)
    search_fields = ('sha256sum',)
    # raw_id_fields = ('os_edition',)
    date_hierarchy = 'created_time'
    formfield_overrides = {
        JSONField: {'widget': JSONEditorWidget(mode='tree')},
    }

    class Meta:
        model = CatalogItem



# @admin.register(OsEdition)
# class OsEditionAdmin(admin.ModelAdmin):
#     list_display = (
#         'os_edition_type', 'os_edition_name', 'os_edition_version',
#         'os_edition_arch', 'os_edition_language', 'created_time', 'updated_time'
#     )
#     list_filter = ('os_edition_arch', 'os_edition_language')
#     search_fields = ('os_edition_type', 'os_edition_name', 'os_edition_version', 'os_edition_arch', 'os_edition_language',)
#
# class OsEditionFilter(AutocompleteFilter):
#     title = 'OS'
#     field_name = 'os_edition'

@admin.register(ManagedItem)
class ManagedItemAdmin(admin.ModelAdmin):
    list_display = ('sha256sum', 'datastore', 'full_path', 'library_item', 'created_time', 'updated_time')
    search_fields = ('sha256sum',)


@admin.register(UpdateTarget)
class UpdateTargetAdmin(admin.ModelAdmin):
    list_display = ('target_name', 'desired_version', 'update_check_frequency', 'catalog_item', 'managed_item', 'created_time', 'updated_time')
