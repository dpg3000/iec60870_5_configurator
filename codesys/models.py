from django.db import models


# Create your models here.
class Map(models.Model):
    Version = models.CharField(max_length=255)
    InputVariable = models.CharField(max_length=255, default="")
    TriggerVariable = models.CharField(max_length=255, default="")
    CheckVariable = models.CharField(max_length=255, default="")
    OutputVariable = models.CharField(max_length=255, default="")
    VariableDeclaration = models.TextField(default="")
    Code = models.TextField(default="")


class Pack(models.Model):
    Version = models.CharField(max_length=255)
    InputVariable = models.CharField(max_length=255, default="")
    OutputVariable = models.CharField(max_length=255, default="")
    VariableDeclaration = models.TextField(default="")
    Code = models.TextField(default="")


class Check(models.Model):
    Version = models.CharField(max_length=255)
    VariableDeclaration = models.TextField(default="")
    Code = models.TextField(default="")


class Save(models.Model):
    Version = models.CharField(max_length=255)
    InputVariable = models.CharField(max_length=255, default="")
    InternalInputVariable = models.CharField(max_length=255, default="")
    HysteresisVariable = models.CharField(max_length=255, default="")
    IteratorVariable = models.CharField(max_length=255, default="")
    VariableDeclaration = models.TextField(default="")
    Code = models.TextField(default="")


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


class Rotate(models.Model):
    Version = models.CharField(max_length=255)
    VariableDeclaration = models.TextField(default="")
    Code = models.TextField(default="")


class Rtu(models.Model):
    Version = models.CharField(max_length=255)
    InputVariable = models.CharField(max_length=255, default="")
    SaveVariable = models.CharField(max_length=255, default="")
    NameVariable = models.CharField(max_length=255, default="")
    TriggerVariable = models.CharField(max_length=255, default="")
    StatusVariable = models.CharField(max_length=255, default="")
    OutputVariable = models.CharField(max_length=255, default="")
    SelectVariable = models.CharField(max_length=255, default="")
    ExecuteVariable = models.CharField(max_length=255, default="")
    SBOErrorVariable = models.CharField(max_length=255, default="")
    VariableDeclaration = models.TextField(default="")


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


class RiseToTrigger(models.Model):
    Version = models.CharField(max_length=255)
    VariableDeclaration = models.TextField(default="")
    Code = models.TextField(default="")
