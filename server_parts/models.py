from django.db import models

DATA_TYPE_CHOICES = (
    ('BOOL', 'BOOL'),
    ('WORD', 'WORD')
)


# Create your models here.
class Server(models.Model):
    Header = models.TextField(default="header")
    ClosingTag = models.TextField(default="closing tag")


class ObjsInfo(models.Model):
    ObjCode = models.CharField(max_length=255)
    ObjInfo = models.TextField()


class Obj35mMeTe(models.Model):
    DeviceName = models.CharField(max_length=255)
    DataType = models.CharField(max_length=255, choices=DATA_TYPE_CHOICES, default="BOOL")
    Hysteresis = models.TextField(blank=True)
    SVA = models.TextField()


class Obj31mDpTb(models.Model):
    DeviceName = models.CharField(max_length=255)
    DataType = models.CharField(max_length=255, choices=DATA_TYPE_CHOICES, default="BOOL")
    DPI = models.TextField()


class Obj58cScTa(models.Model):
    DeviceName = models.CharField(max_length=255)
    DataType = models.CharField(max_length=255, choices=DATA_TYPE_CHOICES, default="BOOL")
    SCS = models.TextField()


class Obj30mSpTb(models.Model):
    DeviceName = models.CharField(max_length=255)
    DataType = models.CharField(max_length=255, choices=DATA_TYPE_CHOICES, default="BOOL")
    SPI = models.TextField()


class Obj59cDcTa(models.Model):
    DeviceName = models.CharField(max_length=255)
    DataType = models.CharField(max_length=255, choices=DATA_TYPE_CHOICES, default="BOOL")
    DCS = models.TextField()
