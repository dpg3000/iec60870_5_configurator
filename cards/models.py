from django.db import models


# Create your models here.
class Card(models.Model):
    Name = models.CharField(max_length=255, default="DI16")
    MonitorIoa = models.IntegerField(default=1000)
    MonitorIoaJump = models.IntegerField(default=100)
    MonitorObjectList = models.TextField(blank=True)
    ControlIoa = models.IntegerField(default=1000)
    ControlIoaJump = models.IntegerField(default=100)
    ControlObjectList = models.TextField(blank=True)
    KbusInfo = models.TextField(default="")


class Kbus(models.Model):
    Headers = models.TextField(default="")
    ClosingTag = models.TextField(default="")
    FinalTerminal = models.TextField(default="")
