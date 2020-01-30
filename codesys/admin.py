from django.contrib import admin
from django.db import models
from .models import Map, Check, Save, Sbo, FBDTemplate, Device, RiseToTrigger, Rtu, UserPrg, FBTemplate


# Register your models here.
# Another way to iterate the meta fields of the models, but if the structure varies, tends to get messy
# class DeviceAdmin(admin.ModelAdmin):
#     fields = (
#         'Version',
#     )
#     field_list = Device._meta.get_fields()
#
#     for index in range(int((len(field_list) - 2) / 2)):
#         field_name = str(field_list[(2 * index) + 2]).split('.')[2]
#         field_name_next = str(field_list[(2 * index) + 3]).split('.')[2]
#         fields = fields + ((field_name, field_name_next),)

class DeviceAdmin(admin.ModelAdmin):
    fieldsets = [
        ("INFO", {"fields": ["Version"]}),
        ("VARIABLE DECLARATION", {"fields": [("SequenceOrder", "SequenceOrderDataType"),
                                             ("Protocol", "ProtocolDataType"),
                                             ("StateLocRem", "StateLocRemDataType"),
                                             ("Measure", "MeasureDataType"),
                                             ("MeasureOutput", "MeasureOutputDataType"),
                                             ("SaveMeasure", "SaveMeasureDataType"),
                                             ("NameMeasure", "NameMeasureDataType"),
                                             ("State", "StateDataType"),
                                             ("StateOutput", "StateOutputDataType"),
                                             ("SaveState", "SaveStateDataType"),
                                             ("NameState", "NameStateDataType"),
                                             ("TriggerState", "TriggerStateDataType"),
                                             ("Command", "CommandDataType"),
                                             ("CommandOutput", "CommandOutputDataType"),
                                             ("SaveCommand", "SaveCommandDataType"),
                                             ("NameCommand", "NameCommandDataType"),
                                             ("TriggerCommand", "TriggerCommandDataType"),
                                             ("Status", "StatusDataType"),
                                             ("Select", "SelectDataType"),
                                             ("Execute", "ExecuteDataType")]})
    ]


class CheckAdmin(admin.ModelAdmin):
    fieldsets = [
        ("INFO", {"fields": ["Version"]}),
        ("VARIABLE DECLARATION", {"fields": [("Iterator", "IteratorDataType"),
                                             ("LastValues", "LastValuesDataType")]}),
        ("CODE", {"fields": ["ST"]})
    ]


class MapAdmin(admin.ModelAdmin):
    fieldsets = [
        ("INFO", {"fields": ["Version"]}),
        ("CODE", {"fields": ["ST"]})
    ]


class RiseAdmin(admin.ModelAdmin):
    fieldsets = [
        ("INFO", {"fields": ["Version"]}),
        ("VARIABLE DECLARATION", {"fields": [("LastRise", "LastRiseDataType"),
                                             ("Iterator", "IteratorDataType")]}),
        ("CODE", {"fields": ["ST"]})
    ]


class RtuAdmin(admin.ModelAdmin):
    fieldsets = [
        ("INFO", {"fields": ["Version"]}),
        ("VARIABLE DECLARATION", {"fields": [("Action", "ActionDataType"),
                                             ("RiseChanges", "RiseChangesDataType"),
                                             ("TriggerChanges", "TriggerChangesDataType"),
                                             ("Signals", "SignalsDataType"),
                                             ("CheckChanges", "CheckChangesDataType"),
                                             ("Names", "NamesDataType"),
                                             ("Saves", "SavesDataType")]})
    ]


class SaveAdmin(admin.ModelAdmin):
    fieldsets = [
        ("INFO", {"fields": ["Version"]}),
        ("VARIABLE DECLARATION", {"fields": [("Time", "TimeDataType"),
                                             ("Offset", "OffsetDataType"),
                                             ("Iterator", "IteratorDataType"),
                                             ("PowerOnPrefix", "PowerOnPrefixDataType", "PowerOnPrefixInitVal"),
                                             ("PrefixUnderLine", "PrefixUnderLineDataType", "PrefixUnderLineInitVal"),
                                             ("Delimiter", "DelimiterDataType", "DelimiterInitVal"),
                                             ("ObjectValue", "ObjectValueDataType"),
                                             ("Prefix", "PrefixDataType"),
                                             ("File", "FileDataType"),
                                             ("Close", "CloseDataType"),
                                             ("NewLine", "NewLineDataType", "NewLineInitVal"),
                                             ("Hysteresis", "HysteresisDataType"),
                                             ("LastValues", "LastValuesDataType")]}),
        ("CODE", {"fields": ["ST"]}),
    ]


class SboAdmin(admin.ModelAdmin):
    fieldsets = [
        ("INFO", {"fields": ["Version"]}),
        ("VARIABLE DECLARATION", {"fields": [("ErrorStatInternal", "ErrorStatInternalDataType"),
                                             ("Flag", "FlagDataType")]}),
        ("CODE", {"fields": ["STBody", "STCore"]})
    ]


class UserPrgAdmin(admin.ModelAdmin):
    fieldsets = [
        ("INFO", {"fields": ["Version"]}),
        ("VARIABLE DECLARATION", {"fields": [("FirstCycle", "FirstCycleDataType"),
                                             ("MaskLocRem", "MaskLocRemDataType"),
                                             ("LocRemState", "LocRemStateDataType")]})
    ]


admin.site.register(Map, MapAdmin)
admin.site.register(Check, CheckAdmin)
admin.site.register(Save, SaveAdmin)
admin.site.register(Sbo, SboAdmin)
admin.site.register(Rtu, RtuAdmin)
admin.site.register(FBDTemplate)
admin.site.register(Device, DeviceAdmin)
admin.site.register(RiseToTrigger, RiseAdmin)
admin.site.register(UserPrg, UserPrgAdmin)
admin.site.register(FBTemplate)
