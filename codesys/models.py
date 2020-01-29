from django.db import models


# Create your models here.
class Rtu(models.Model):
    Version = models.CharField(max_length=255)
    Action = models.CharField(max_length=255, default="")
    ActionDataType = models.CharField(max_length=255, default="")
    RiseChanges = models.CharField(max_length=255, default="")
    RiseChangesDataType = models.CharField(max_length=255, default="")
    TriggerChanges = models.CharField(max_length=255, default="")
    TriggerChangesDataType = models.CharField(max_length=255, default="")
    Signals = models.CharField(max_length=255, default="")
    SignalsDataType = models.CharField(max_length=255, default="")
    CheckChanges = models.CharField(max_length=255, default="")
    CheckChangesDataType = models.CharField(max_length=255, default="")
    Names = models.CharField(max_length=255, default="")
    NamesDataType = models.CharField(max_length=255, default="")
    Saves = models.CharField(max_length=255, default="")
    SavesDataType = models.CharField(max_length=255, default="")

    def __str__(self):
        return self.Version


class Map(models.Model):
    Version = models.CharField(max_length=255)
    ST = models.TextField(default="")

    def __str__(self):
        return self.Version


class Check(models.Model):
    Version = models.CharField(max_length=255)
    Iterator = models.CharField(max_length=255, default="")
    IteratorDataType = models.CharField(max_length=255, default="")
    LastValues = models.CharField(max_length=255, default="")
    LastValuesDataType = models.CharField(max_length=255, default="")
    ST = models.TextField()

    def __str__(self):
        return self.Version


class Save(models.Model):
    Version = models.CharField(max_length=255)
    Time = models.CharField(max_length=255, default="")
    TimeDataType = models.CharField(max_length=255, default="")
    Offset = models.CharField(max_length=255, default="")
    OffsetDataType = models.CharField(max_length=255, default="")
    Iterator = models.CharField(max_length=255, default="")
    IteratorDataType = models.CharField(max_length=255, default="")
    PowerOnPrefix = models.CharField(max_length=255, default="")
    PowerOnPrefixDataType = models.CharField(max_length=255, default="")
    PowerOnPrefixInitVal = models.CharField(max_length=255, default="")
    PrefixUnderLine = models.CharField(max_length=255, default="")
    PrefixUnderLineDataType = models.CharField(max_length=255, default="")
    PrefixUnderLineInitVal = models.CharField(max_length=255, default="")
    Delimiter = models.CharField(max_length=255, default="")
    DelimiterDataType = models.CharField(max_length=255, default="")
    DelimiterInitVal = models.CharField(max_length=255, default="")
    ObjectValue = models.CharField(max_length=255, default="")
    ObjectValueDataType = models.CharField(max_length=255, default="")
    Prefix = models.CharField(max_length=255, default="")
    PrefixDataType = models.CharField(max_length=255, default="")
    File = models.CharField(max_length=255, default="")
    FileDataType = models.CharField(max_length=255, default="")
    Close = models.CharField(max_length=255, default="")
    CloseDataType = models.CharField(max_length=255, default="")
    NewLine = models.CharField(max_length=255, default="")
    NewLineDataType = models.CharField(max_length=255, default="")
    NewLineInitVal = models.CharField(max_length=255, default="")
    Hysteresis = models.CharField(max_length=255, default="")
    HysteresisDataType = models.CharField(max_length=255, default="")
    LastValues = models.CharField(max_length=255, default="")
    LastValuesDataType = models.CharField(max_length=255, default="")
    ST = models.TextField(default="")

    def __str__(self):
        return self.Version


class Sbo(models.Model):
    Version = models.CharField(max_length=255)
    ErrorStatInternal = models.CharField(max_length=255, default="")
    ErrorStatInternalDataType = models.CharField(max_length=255, default="")
    Flag = models.CharField(max_length=255, default="")
    FlagDataType = models.CharField(max_length=255, default="")
    STBody = models.TextField(default="")
    STCore = models.TextField(default="")

    def __str__(self):
        return self.Version


class FbdTemplate(models.Model):
    Header = models.TextField(default="")
    InputHeader = models.TextField(default="")
    InputUnit = models.TextField(default="")
    OutputHeader = models.TextField(default="")
    OutputUnit = models.TextField(default="")


class Device(models.Model):
    Version = models.CharField(max_length=255, default="")
    SequenceOrder = models.CharField(max_length=255, default="")
    SequenceOrderDataType = models.CharField(max_length=255, default="")
    Protocol = models.CharField(max_length=255, default="")
    ProtocolDataType = models.CharField(max_length=255, default="")
    StateLocRem = models.CharField(max_length=255, default="")
    StateLocRemDataType = models.CharField(max_length=255, default="")

    Measure = models.CharField(max_length=255, default="")
    MeasureDataType = models.CharField(max_length=255, default="")
    MeasureOutput = models.CharField(max_length=255, default="")
    MeasureOutputDataType = models.CharField(max_length=255, default="")
    SaveMeasure = models.CharField(max_length=255, default="")
    SaveMeasureDataType = models.CharField(max_length=255, default="")
    NameMeasure = models.CharField(max_length=255, default="")
    NameMeasureDataType = models.CharField(max_length=255, default="")

    State = models.CharField(max_length=255, default="")
    StateDataType = models.CharField(max_length=255, default="")
    StateOutput = models.CharField(max_length=255, default="")
    StateOutputDataType = models.CharField(max_length=255, default="")
    SaveState = models.CharField(max_length=255, default="")
    SaveStateDataType = models.CharField(max_length=255, default="")
    NameState = models.CharField(max_length=255, default="")
    NameStateDataType = models.CharField(max_length=255, default="")
    TriggerState = models.CharField(max_length=255, default="")
    TriggerStateDataType = models.CharField(max_length=255, default="")

    Command = models.CharField(max_length=255, default="")
    CommandDataType = models.CharField(max_length=255, default="")
    CommandOutput = models.CharField(max_length=255, default="")
    CommandOutputDataType = models.CharField(max_length=255, default="")
    SaveCommand = models.CharField(max_length=255, default="")
    SaveCommandDataType = models.CharField(max_length=255, default="")
    NameCommand = models.CharField(max_length=255, default="")
    NameCommandDataType = models.CharField(max_length=255, default="")
    TriggerCommand = models.CharField(max_length=255, default="")
    TriggerCommandDataType = models.CharField(max_length=255, default="")
    Status = models.CharField(max_length=255, default="")
    StatusDataType = models.CharField(max_length=255, default="")
    Select = models.CharField(max_length=255, default="")
    SelectDataType = models.CharField(max_length=255, default="")
    Execute = models.CharField(max_length=255, default="")
    ExecuteDataType = models.CharField(max_length=255, default="")

    def __str__(self):
        return self.Version


class RiseToTrigger(models.Model):
    Version = models.CharField(max_length=255)
    LastRise = models.CharField(max_length=255, default="")
    LastRiseDataType = models.CharField(max_length=255, default="")
    Iterator = models.CharField(max_length=255, default="")
    IteratorDataType = models.CharField(max_length=255, default="")
    ST = models.TextField(default="")

    def __str__(self):
        return self.Version


class UserPrg(models.Model):
    Version = models.CharField(max_length=255)
    FirstCycle = models.CharField(max_length=255, default="")
    FirstCycleDataType = models.CharField(max_length=255, default="")

    def __str__(self):
        return self.Version


class STTemplate(models.Model):
    DeclarationAttributes = models.TextField(default="")
    DeclarationFBHeader = models.CharField(max_length=255, default="")
    DeclarationFHeader = models.CharField(max_length=255, default="")
    DeclarationInput = models.TextField(default="")
    DeclarationOutput = models.TextField(default="")
    DeclarationInternal = models.TextField(default="")
    DeclarationEndTag = models.CharField(max_length=255, default="")
    CodeEndTag = models.CharField(max_length=255, default="")
