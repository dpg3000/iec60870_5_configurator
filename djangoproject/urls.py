"""djxml104 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from devs.views import configurator_view, submit, validate_parameters
from codesys import models

urlpatterns = [
    path('configurator/', configurator_view),
    path('admin/', admin.site.urls),
    path('configurator/submit/', submit),
    path('ajax/validate_parameters/', validate_parameters),
]

# Filling interface for pou management at runserver
models.fbd_model = models.FunctionBlockDiagramModel()
models.fb_model = models.FunctionBlockModel()
models.user_prg_model = models.UserPrgModel(models.fbd_model, models.user_prg_version)
models.device_model = models.DeviceModel(models.user_prg_model, models.device_version)
models.rtu_model = models.RtuModel(models.device_model, models.rtu_version)
models.pack_model = models.PackModel(models.rtu_model, models.fb_model, models.pack_version)
models.check_model = models.CheckModel(models.rtu_model, models.fb_model, models.check_version)
models.map_model = models.MapModel(models.rtu_model, models.fb_model, models.map_version)
models.rise_model = models.RiseModel(models.rtu_model, models.fb_model, models.rise_version)
models.save_model = models.SaveModel(models.rtu_model, models.fb_model, models.save_version)



