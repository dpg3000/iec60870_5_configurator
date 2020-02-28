from django.contrib import admin
from .models import Device


class DeviceAdmin(admin.ModelAdmin):
    fieldsets = [
        ("INFO", {"fields": ["Name", "Protocol"]}),
        ("OPERATION", {"fields": ["DO", "SBO"]}),
        ("MONITOR", {"fields": ["MonitorIoa", "MonitorIoaJump", "MonitorObjectList"]}),
        ("CONTROL", {"fields": ["ControlIoa", "ControlIoaJump", "ControlObjectList"]}),
    ]


admin.site.register(Device, DeviceAdmin)


