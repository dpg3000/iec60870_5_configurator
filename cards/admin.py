from django.contrib import admin
from .models import Card, Kbus


class CardAdmin(admin.ModelAdmin):
    fieldsets = [
        ("INFO", {"fields": ["Name"]}),
        ("MONITOR", {"fields": ["MonitorIoa", "MonitorIoaJump", "MonitorObjectList"]}),
        ("CONTROL", {"fields": ["ControlIoa", "ControlIoaJump", "ControlObjectList"]}),
        ("KBUS", {"fields": ["KbusInfo"]})
    ]


# Register your models here.
admin.site.register(Card, CardAdmin)
admin.site.register(Kbus)
