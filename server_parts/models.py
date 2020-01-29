from django.db import models

OBJ_TYPE_CHOICES = (
    ('MONITOR', 'MONITOR'),
    ('CONTROL', 'CONTROL')
)

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
    ObjType = models.CharField(max_length=255, choices=OBJ_TYPE_CHOICES, default=1)

    class Meta:
        verbose_name_plural = "objInfo"

    def __str__(self):
        return self.ObjCode


class Obj35mMeTe(models.Model):
    DeviceName = models.CharField(max_length=255)
    DataType = models.CharField(max_length=255, choices=DATA_TYPE_CHOICES, default="BOOL")
    Hysteresis = models.TextField(blank=True)
    SVA = models.TextField()

    class Meta:
        verbose_name_plural = "obj_35m_me_te"

    def __str__(self):
        return self.DeviceName


class Obj31mDpTb(models.Model):
    DeviceName = models.CharField(max_length=255)
    DataType = models.CharField(max_length=255, choices=DATA_TYPE_CHOICES, default="BOOL")
    DPI = models.TextField()

    class Meta:
        verbose_name_plural = "obj_31m_dp_tb"

    def __str__(self):
        return self.DeviceName


class Obj58cScTa(models.Model):
    DeviceName = models.CharField(max_length=255)
    DataType = models.CharField(max_length=255, choices=DATA_TYPE_CHOICES, default="BOOL")
    SCS = models.TextField()

    class Meta:
        verbose_name_plural = "obj_58c_sc_ta"

    def __str__(self):
        return self.DeviceName


class Obj30mSpTb(models.Model):
    DeviceName = models.CharField(max_length=255)
    DataType = models.CharField(max_length=255, choices=DATA_TYPE_CHOICES, default="BOOL")
    SPI = models.TextField()

    class Meta:
        verbose_name_plural = "obj_30m_sp_tb"

    def __str__(self):
        return self.DeviceName


class Obj59cDcTa(models.Model):
    DeviceName = models.CharField(max_length=255)
    DataType = models.CharField(max_length=255, choices=DATA_TYPE_CHOICES, default="BOOL")
    DCS = models.TextField()

    class Meta:
        verbose_name_plural = "obj_59c_dc_ta"

    def __str__(self):
        return self.DeviceName
