from django.contrib import admin
from .models import Card, Kbus


class CardAdmin(admin.ModelAdmin):
    fieldsets = [
        ("INFO", {"fields": ["ArticleNo",
                             ("SubBusName", "IO"),
                             ("ModuleType", "ModuleChannels")]}),
        ("MONITOR", {"fields": ["MonitorIoa", "MonitorIoaJump", "MonitorObjectList"]}),
        ("CONTROL", {"fields": ["ControlIoa", "ControlIoaJump", "ControlObjectList"]})
    ]


# Register your models here.
admin.site.register(Card, CardAdmin)
admin.site.register(Kbus)
