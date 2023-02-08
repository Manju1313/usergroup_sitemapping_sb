from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin, ImportExportMixin
from import_export.formats import base_formats
from import_export import resources, fields
from import_export.fields import Field

# Register your models here.
class ImportExportFormat(ImportExportMixin):
    def get_export_formats(self):
        formats = (base_formats.CSV, base_formats.XLSX, base_formats.XLS,)
        return [f for f in formats if f().can_export()]

    def get_import_formats(self):
        formats = (base_formats.CSV, base_formats.XLSX, base_formats.XLS,)
        return [f for f in formats if f().can_import()]


admin.site.site_url = "cric1"


@admin.register(UserSiteMapping)
class UserSiteMappingAdmin(ImportExportModelAdmin, ImportExportFormat):
    list_display = ['user', 'site', 'status' ]
    fields = ['user', 'site', 'status']
    search_fields = ['user__username', ]
    list_per_page = 15

admin.site.register(NoteModel)


@admin.register(Employee)
class EmployeeAdmin(ImportExportModelAdmin, ImportExportFormat):
    list_display = ['first_name', 'last_name', 'mobile','email' ]
    fields = ['first_name', 'last_name', 'mobile','email' ]
    search_fields = ['first_name', 'last_name']
    list_per_page = 15

