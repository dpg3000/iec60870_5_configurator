from django.db import models


# Create your models here.
class Project(models.Model):
    Header = models.TextField(default="header")
    ClosingTag = models.TextField(default="closing tag")
