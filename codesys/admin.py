from django.contrib import admin
from django.db import models
from .models import Map, Check, Save, Sbo, FBDTemplate, Device, RiseToTrigger, Rtu, UserPrg, Pack, Handler, \
    PackLocRem, CheckLocRem


# Register your models here.
class UserPrgAdmin(admin.ModelAdmin):
    fieldsets = [
        ("INFO", {"fields": ["Version",
                             ("ProgramHeader", "ProgramEndTag")]}),
        ("VARIABLE DECLARATION", {"fields": [("FirstCycle", "FirstCycleDataType", "FirstCycleInitVal"),
                                             ("MaskLocRem", "MaskLocRemDataType"),
                                             ("StateLocRem", "StateLocRemDataType"),
                                             ("DummyMeasure", "DummyMeasureDataType"),
                                             ("DummyMeasureOutput", "DummyMeasureOutputDataType"),
                                             ("DummyState", "DummyStateDataType"),
                                             ("DummyStateOutput", "DummyStateOutputDataType"),
                                             ("DummyCommand", "DummyCommandDataType"),
                                             ("DummyCommandOutput", "DummyCommandOutputDataType"),
                                             ("DummyStatus", "DummyStatusDataType"),
                                             ("DummySelect", "DummySelectDataType"),
                                             ("DummyExecute", "DummyExecuteDataType")]})
    ]


class PackLocRemAdmin(admin.ModelAdmin):
    fieldsets = [
        ("INFO", {"fields": ["Version"]}),
        ("VARIABLE DECLARATION", {"fields": [("LocRemInput", "LocRemInputDataType"),
                                             ("LocRemOutput", "LocRemOutputDataType")]}),
        ("CODE", {"fields": ["ST"]})
    ]


class CheckLocRemAdmin(admin.ModelAdmin):
    fieldsets = [
        ("INFO", {"fields": ["Version"]}),
        ("VARIABLE DECLARATION", {"fields": [("Iterator", "IteratorDataType")]}),
        ("CODE", {"fields": ["ST"]})
    ]


class DeviceAdmin(admin.ModelAdmin):
    fieldsets = [
        ("INFO", {"fields": ["Version"]}),
        ("VARIABLE DECLARATION", {"fields": [("SequenceOrder", "SequenceOrderDataType"),
                                             ("Protocol", "ProtocolDataType"),
                                             ("Measure", "MeasureDataType"),
                                             ("MeasureOutput", "MeasureOutputDataType"),
                                             ("SaveMeasure", "SaveMeasureDataType"),
                                             ("NameMeasure", "NameMeasureDataType"),
                                             ("State", "StateDataType"),
                                             ("StateOutput", "StateOutputDataType"),
                                             ("SaveState", "SaveStateDataType"),
                                             ("NameState", "NameStateDataType"),
                                             ("RiseState", "RiseStateDataType"),
                                             ("Command", "CommandDataType"),
                                             ("CommandOutput", "CommandOutputDataType"),
                                             ("SaveCommand", "SaveCommandDataType"),
                                             ("NameCommand", "NameCommandDataType"),
                                             ("TriggerCommand", "TriggerCommandDataType"),
                                             ("Status", "StatusDataType"),
                                             ("Select", "SelectDataType"),
                                             ("Execute", "ExecuteDataType")]})
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
                                             ("Saves", "SavesDataType"),
                                             ("Error", "ErrorDataType")]})
    ]


class RiseAdmin(admin.ModelAdmin):
    fieldsets = [
        ("INFO", {"fields": ["Version"]}),
        ("VARIABLE DECLARATION", {"fields": [("LastRise", "LastRiseDataType"),
                                             ("Iterator", "IteratorDataType")]}),
        ("CODE", {"fields": ["ST"]})
    ]


class PackAdmin(admin.ModelAdmin):
    fieldsets = [
        ("INFO", {"fields": ["Version"]}),
        ("CODE", {"fields": ["ST"]})
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


class SaveAdmin(admin.ModelAdmin):
    fieldsets = [
        ("INFO", {"fields": ["Version"]}),
        ("VARIABLE DECLARATION", {"fields": [("Reason", "ReasonDataType", "ReasonInitVal"),
                                             ("Time", "TimeDataType"),
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


class HandlerAdmin(admin.ModelAdmin):
    fieldsets = [
        ("INFO", {"fields": ["Version"]}),
        ("VARIABLE DECLARATION", {"fields": [("ErrorDescription", "ErrorDescriptionDataType")]}),
        ("CODE", {"fields": ["ST"]})
    ]


admin.site.register(FBDTemplate)
admin.site.register(UserPrg, UserPrgAdmin)
admin.site.register(PackLocRem, PackLocRemAdmin)
admin.site.register(CheckLocRem, CheckLocRemAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(Rtu, RtuAdmin)
admin.site.register(RiseToTrigger, RiseAdmin)
admin.site.register(Pack, PackAdmin)
admin.site.register(Check, CheckAdmin)
admin.site.register(Map, MapAdmin)
admin.site.register(Save, SaveAdmin)
admin.site.register(Sbo, SboAdmin)
admin.site.register(Handler, HandlerAdmin)
