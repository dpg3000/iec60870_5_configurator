from django.db import models
from multiselectfield import MultiSelectField
from server_parts.models import ObjsInfo


IO_CHOICES = (
    ('DI', 'DI'),
    ('DO', 'DO')
)


MONITOR_OBJ_CHOICES = ()
CONTROL_OBJ_CHOICES = ()

for m in ObjsInfo.objects.all():
    if m.ObjType == 'MONITOR':
        MONITOR_OBJ_CHOICES = MONITOR_OBJ_CHOICES + ((m.ObjCode, m.ObjCode),)
    if m.ObjType == 'CONTROL':
        CONTROL_OBJ_CHOICES = CONTROL_OBJ_CHOICES + ((m.ObjCode, m.ObjCode),)


# Create your models here.
class Card(models.Model):
    ArticleNo = models.CharField(max_length=255, default="")
    SubBusName = models.CharField(max_length=255, default="")
    ModuleType = models.CharField(max_length=255, default="")
    ModuleChannels = models.CharField(max_length=255, default="")
    IO = models.CharField(max_length=255, choices=IO_CHOICES, default="")
    MonitorIoa = models.IntegerField(blank=True)
    MonitorIoaJump = models.IntegerField(blank=True)
    MonitorObjectList = MultiSelectField(choices=MONITOR_OBJ_CHOICES, blank=True)
    ControlIoa = models.IntegerField(blank=True)
    ControlIoaJump = models.IntegerField(blank=True)
    ControlObjectList = MultiSelectField(choices=CONTROL_OBJ_CHOICES, blank=True)

    def __str__(self):
        return self.ArticleNo


class Kbus(models.Model):
    Body = models.TextField(default="")
    Terminal = models.TextField(default="")
    DISignal = models.CharField(max_length=255, default="")
    PrivateInputChannel = models.TextField(default="")
    PublicInputChannel = models.TextField(default="")
    DOSignal = models.CharField(max_length=255, default="")
    PrivateOutputChannel = models.TextField(default="")
    PublicOutputChannel = models.TextField(default="")

    class Meta:
        verbose_name_plural = "Kbus"
