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

CLIENT_CHOICES = (
    ('yes', 'yes'),
    ('no', 'no')
)

SERVER_CHOICES = (
    ('yes', 'yes'),
    ('no', 'no')
)

PROTOCOL_CHOICES = (
    ('MODBUS_TCP', 'MODBUS_TCP'),
    ('IEC_103', 'IEC_103'),
    ('IEC_104', 'IEC_104')
)


# Create your models here.
class Device(models.Model):
    Name = models.CharField(max_length=255, default="7SJ6x")
    DO = models.BooleanField(default=False)
    SBO = models.BooleanField(default=False)
    Protocol = models.CharField(max_length=255, choices=PROTOCOL_CHOICES, default="104")
    MonitorIoa = models.IntegerField(default=1000)
    MonitorIoaJump = models.IntegerField(default=100)
    MonitorObjectList = MultiSelectField(choices=MONITOR_OBJ_CHOICES, blank=True)
    ControlIoa = models.IntegerField(default=1000)
    ControlIoaJump = models.IntegerField(default=100)
    ControlObjectList = MultiSelectField(choices=CONTROL_OBJ_CHOICES, blank=True)
    ClientObjs = models.TextField(blank=True)
    ClientSignals = models.TextField(blank=True)

    def __str__(self):
        return self.Name
