from django.contrib import admin
from .models import Map, Pack, Check, Save, Sbo, Rotate, FbdTemplate, Device, RiseToTrigger, Rtu


# Register your models here.
class DeviceAdmin(admin.ModelAdmin):
    fields = (
        'Version',
    )
    field_list = Device._meta.get_fields()

    for index in range(int((len(field_list) - 2) / 2)):
        field_name = str(field_list[(2 * index) + 2]).split('.')[2]
        field_name_next = str(field_list[(2 * index) + 3]).split('.')[2]
        fields = fields + ((field_name, field_name_next),)


class RtuAdmin(admin.ModelAdmin):
    fields = (
        'Version',
    )
    field_list = Rtu._meta.get_fields()

    for index in range(int((len(field_list) - 2) / 2)):
        field_name = str(field_list[(2 * index) + 2]).split('.')[2]
        field_name_next = str(field_list[(2 * index) + 3]).split('.')[2]
        fields = fields + ((field_name, field_name_next),)


admin.site.register(Map)
admin.site.register(Pack)
admin.site.register(Check)
admin.site.register(Save)
admin.site.register(Sbo)
admin.site.register(Rotate)
admin.site.register(Rtu, RtuAdmin)
admin.site.register(FbdTemplate)
admin.site.register(Device, DeviceAdmin)
admin.site.register(RiseToTrigger)
