from django.db import models


# Create your models here.
class Rtu(models.Model):
    Version = models.CharField(max_length=255)
    InputVariable = models.CharField(max_length=255, default="")
    OutputVariable = models.CharField(max_length=255, default="")
    OutputPackVariable = models.CharField(max_length=255, default="")
    SaveInputVariable = models.CharField(max_length=255, default="")
    SaveOutputVariable = models.CharField(max_length=255, default="")
    NameInputVariable = models.CharField(max_length=255, default="")
    NameOutputVariable = models.CharField(max_length=255, default="")
    TriggerInputVariable = models.CharField(max_length=255, default="")
    TriggerOutputVariable = models.CharField(max_length=255, default="")
    StatusVariable = models.CharField(max_length=255, default="")
    SelectVariable = models.CharField(max_length=255, default="")
    ExecuteVariable = models.CharField(max_length=255, default="")
    SBOErrorVariable = models.CharField(max_length=255, default="")
    VariableDeclaration = models.TextField(default="")

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
    rtu = models.ForeignKey(Rtu, default=1, verbose_name="parent", on_delete=models.SET_DEFAULT)

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
    Version = models.CharField(max_length=255)
    VariableDeclaration = models.TextField(default="")
    Code = models.TextField(default="")

    def __str__(self):
        return self.Version


class RiseToTrigger(models.Model):
    Version = models.CharField(max_length=255)
    VariableDeclaration = models.TextField(default="")
    Code = models.TextField(default="")

    def __str__(self):
        return self.Version
