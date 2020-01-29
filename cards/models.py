from django.db import models
from multiselectfield import MultiSelectField
from server_parts.models import ObjsInfo


MONITOR_OBJ_CHOICES = ()
CONTROL_OBJ_CHOICES = ()

for m in ObjsInfo.objects.all():
    if m.ObjType == 'MONITOR':
        MONITOR_OBJ_CHOICES = MONITOR_OBJ_CHOICES + ((m.ObjCode, m.ObjCode),)
    if m.ObjType == 'CONTROL':
        CONTROL_OBJ_CHOICES = CONTROL_OBJ_CHOICES + ((m.ObjCode, m.ObjCode),)


# Create your models here.
class Card(models.Model):
    Name = models.CharField(max_length=255, default="DI16")
    MonitorIoa = models.IntegerField(blank=True)
    MonitorIoaJump = models.IntegerField(blank=True)
    MonitorObjectList = MultiSelectField(choices=MONITOR_OBJ_CHOICES, blank=True)
    ControlIoa = models.IntegerField(blank=True)
    ControlIoaJump = models.IntegerField(blank=True)
    ControlObjectList = MultiSelectField(choices=CONTROL_OBJ_CHOICES, blank=True)
    KbusInfo = models.TextField(default="")

    def __str__(self):
        return self.Name


class Kbus(models.Model):
    Headers = models.TextField(default="")
    ClosingTag = models.TextField(default="")
    FinalTerminal = models.TextField(default="")

    class Meta:
        verbose_name_plural = "Kbus"
