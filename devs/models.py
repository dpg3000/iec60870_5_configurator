from django.db import models

CLIENT_CHOICES = (
    ('yes', 'yes'),
    ('no', 'no')
)

SERVER_CHOICES = (
    ('yes', 'yes'),
    ('no', 'no')
)

PROTOCOL_CHOICES = (
    ('MODBUS', 'MODBUS'),
    ('103', '103'),
    ('104', '104')
)


# Create your models here.
class Device(models.Model):
    Name = models.CharField(max_length=255, default="7SJ6x")
    DO = models.BooleanField(default=False)
    SBO = models.BooleanField(default=False)
    Protocol = models.CharField(max_length=255, choices=PROTOCOL_CHOICES, default="104")
    MonitorIoa = models.IntegerField(default=1000)
    MonitorIoaJump = models.IntegerField(default=100)
    MonitorObjectList = models.CharField(blank=True, max_length=255)
    ControlIoa = models.IntegerField(default=1000)
    ControlIoaJump = models.IntegerField(default=100)
    ControlObjectList = models.CharField(blank=True, max_length=255)
    ClientObjs = models.TextField(blank=True)
    ClientSignals = models.TextField(blank=True)
