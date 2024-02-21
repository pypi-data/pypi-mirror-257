from django.contrib import admin
from .models import Applicant, Voucher, Program, Application
from import_export.admin import ImportExportModelAdmin
# Register your models here.

class VoucherAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('code', 'active')
    

admin.site.register(Applicant)
admin.site.register(Voucher, VoucherAdmin)
admin.site.register(Program)
admin.site.register(Application)
