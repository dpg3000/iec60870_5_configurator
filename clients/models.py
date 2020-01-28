from django.db import models


# Create your models here.
class Client(models.Model):
    Protocol = models.CharField(max_length=255)
    Headers = models.TextField(default="")
    ConnectionHeaders = models.TextField(default="")
    ClosingTag = models.TextField(default="")


