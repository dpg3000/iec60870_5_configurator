from django.db import models


# Create your models here.
class Rtu(models.Model):
    Version = models.CharField(max_length=255)
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
    InputVariable = models.CharField(max_length=255, default="")
    TriggerVariable = models.CharField(max_length=255, default="")
    CheckVariable = models.CharField(max_length=255, default="")
    OutputVariable = models.CharField(max_length=255, default="")
    VariableDeclaration = models.TextField(default="")
    Code = models.TextField(default="")

    def __str__(self):
        return self.Version


class Pack(models.Model):
    Version = models.CharField(max_length=255)
    InputVariable = models.CharField(max_length=255, default="")
    OutputVariable = models.CharField(max_length=255, default="")
    VariableDeclaration = models.TextField(default="")
    Code = models.TextField(default="")

    def __str__(self):
        return self.Version


class Check(models.Model):
    Version = models.CharField(max_length=255)
    VariableDeclaration = models.TextField(default="")
    Code = models.TextField(default="")

    def __str__(self):
        return self.Version


class Save(models.Model):
    Version = models.CharField(max_length=255)
    InputVariable = models.CharField(max_length=255, default="")
    InternalInputVariable = models.CharField(max_length=255, default="")
    HysteresisVariable = models.CharField(max_length=255, default="")
    IteratorVariable = models.CharField(max_length=255, default="")
    VariableDeclaration = models.TextField(default="")
    Code = models.TextField(default="")

    def __str__(self):
        return self.Version


class Sbo(models.Model):
    Version = models.CharField(max_length=255)
    InputVariable = models.CharField(max_length=255, default="")
    StatusVariable = models.CharField(max_length=255, default="")
    SelectVariable = models.CharField(max_length=255, default="")
    ExecuteVariable = models.CharField(max_length=255, default="")
    FlagVariable = models.CharField(max_length=255, default="")
    VariableDeclaration = models.TextField(default="")
    Body = models.TextField(default="")
    Core = models.TextField(default="")
    FinalCheck = models.TextField(default="")

    def __str__(self):
        return self.Version


class Rotate(models.Model):
    Version = models.CharField(max_length=255)
    VariableDeclaration = models.TextField(default="")
    Code = models.TextField(default="")

    def __str__(self):
        return self.Version


class FbdTemplate(models.Model):
    Header = models.TextField(default="")
    InputHeader = models.TextField(default="")
    InputUnit = models.TextField(default="")
    OutputHeader = models.TextField(default="")
    OutputUnit = models.TextField(default="")
    Jump = models.TextField(default="")


class Device(models.Model):
    Version = models.CharField(max_length=255, default="")
    FirstCycle = models.CharField(max_length=255, default="")
    FirstCycleDataType = models.CharField(max_length=255, default="")
    SequenceOrder = models.CharField(max_length=255, default="")
    SequenceOrderDataType = models.CharField(max_length=255, default="")
    Protocol = models.CharField(max_length=255, default="")
    ProtocolDataType = models.CharField(max_length=255, default="")
    StateLR = models.CharField(max_length=255, default="")
    StateLRDataType = models.CharField(max_length=255, default="")
    Action = models.CharField(max_length=255, default="")
    ActionDataType = models.CharField(max_length=255, default="")

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
    VariableDeclaration = models.TextField(default="")
    Code = models.TextField(default="")

    def __str__(self):
        return self.Version
