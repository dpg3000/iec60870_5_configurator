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
import pou
from codesys import models

urlpatterns = [
    path('configurator/', configurator_view),
    path('admin/', admin.site.urls),
    path('configurator/submit/', submit),
    path('ajax/validate_parameters/', validate_parameters),
]

# Filling interface for pou management at runserver
pou.fbd_model = models.FunctionBlockDiagramModel()
pou.user_prg_model = models.UserPrgModel(pou.fbd_model, models.user_prg_version)
pou.device_model = models.DeviceModel(pou.user_prg_model, models.device_version)
pou.rtu_model = models.RtuModel(pou.device_model, models.rtu_version)
pou.pack_model = models.PackModel(pou.rtu_model, models.pack_version)
pou.check_model = models.CheckModel(pou.rtu_model, models.check_version)
pou.map_model = models.MapModel(pou.rtu_model, models.map_version)
pou.rise_model = models.RiseModel(pou.rtu_model, models.rise_version)
pou.save_model = models.SaveModel(pou.rtu_model, models.save_version)
pou.sbo_model = models.SboModel(pou.sbo_model, models.sbo_version)
pou.handler_model = models.HandlerModel(pou.rtu_model, models.handler_version)


