from django.contrib import admin
from visit_analytics.models import Worker, Unit, Visit


class WorkerAdmin(admin.ModelAdmin):
    search_fields = ['name']


class UnitAdmin(admin.ModelAdmin):
    search_fields = ['name']


class VisitAdmin(admin.ModelAdmin):
    search_fields = ['unit__worker__name', 'unit__name']
    readonly_fields = ['time_stamp', 'unit', 'latitude', 'longitude']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Worker, WorkerAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Visit, VisitAdmin)
