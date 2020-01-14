from django.contrib import admin
from .models import Map, Pack, Check, Save, Sbo, Rotate, Rtu, FbdTemplate, Device

# Register your models here.
admin.site.register(Map)
admin.site.register(Pack)
admin.site.register(Check)
admin.site.register(Save)
admin.site.register(Sbo)
admin.site.register(Rotate)
admin.site.register(Rtu)
admin.site.register(FbdTemplate)
admin.site.register(Device)