import xml.etree.ElementTree as ET
import zipfile
from django.shortcuts import render
from devs.models import Device
from cards.models import Card
import os
from django.http import HttpResponse, HttpResponseNotFound
import datetime
from server import Server, ServerDevice, ServerCard
from project import Project
import client
from client import Client
from kbus import Kbus
import kbus
from django.http import JsonResponse
import pou
import shutil

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Create your views here.
def configurator_view(request, *args, **kwargs):
    devices = Device.objects.all()
    cards = Card.objects.all()
    devices_num = devices.count()
    cards_num = cards.count()

    my_context = {
        "devices": devices,
        "cards": cards,
        "devices_num": devices_num,
        "cards_num": cards_num
    }

    return render(request, "configurator.html", my_context)


def validate_parameters(request):
    device_name = request.GET.get('device_name', None)

    client_existence = Device.objects.filter(Name=device_name).first().ClientObjs
    if client_existence:
        client_existence = True
    else:
        client_existence = False

    do_capability = Device.objects.filter(Name=device_name).first().DO
    sbo_capability = Device.objects.filter(Name=device_name).first().SBO

    data = {
        'is_client': client_existence,
        'is_do': do_capability,
        'is_sbo': sbo_capability
    }

    return JsonResponse(data)


def submit(request):
    # Paths to files
    fl_iec60870_5_config = os.path.abspath("iec60870_5_configuration.xml")
    fl_k_bus = os.path.abspath("k_bus_configuration.xml")
    fl_pou_files = os.path.abspath("POUs")

    # Initial erase to avoid partial overwriting
    if os.path.isfile(fl_iec60870_5_config):
        os.remove(fl_iec60870_5_config)

    if os.path.isfile(fl_k_bus):
        os.remove(fl_k_bus)

    # Open file to write (w+ -> if the file doesn't exist, it is created)
    iec60870_5_config = open("iec60870_5_configuration.xml", "w+")
    k_bus = open("k_bus_configuration.xml", "w+")

    # Project header with time stamp
    project = Project(datetime.datetime.now())
    project.headers(iec60870_5_config)

    # Parsing xml from form data
    raw_xml = request.POST.get('request-data')
    root = ET.fromstring(raw_xml)

    # iterating over parsed xml to create the server instances
    server_iteration = 0
    pou.delete_pous()
    for center in root.iter('center'):
        center_ins = Server(center.attrib['name'], server_iteration)
        center_ins.headers(iec60870_5_config)
        for card in center.iter('card'):
            if card.attrib['server'] == 'yes':
                card_ins = ServerCard(card.text, server_iteration)
                card_ins.create_card(int(card.attrib['number']), iec60870_5_config)
            if card.attrib['io'] == 'yes':
                kbus_ins = Kbus(card.text)
                kbus_ins.create_kbus(int(card.attrib['number']))
        for device in center.iter('device'):
            if device.attrib['server'] == 'yes':
                device_ins = ServerDevice(device.text, server_iteration)
                error_message = device_ins.create_device(int(device.attrib['number']), iec60870_5_config)
                if error_message:
                    return HttpResponse("<h1>" + error_message + "</h1>")
            if device.attrib['client'] == 'yes':
                client_ins = Client(device.text)
                client_ins.create_client(int(device.attrib['number']))
            error_message = pou.create_pou(device.text, int(device.attrib['number']), device.attrib['operation'],
                                           server_iteration)
            if error_message:
                return HttpResponse("<h1>" + error_message + "</h1>")
        server_iteration += 1
        # server closing tags
        center_ins.closing_tags(iec60870_5_config)
    # Creating user-prg
    # pou.user_prg()
    # write client instances
    client.write_client(iec60870_5_config)
    client.clear_class_variables()
    # write k-bus instances
    kbus.write_kbus(k_bus)
    kbus.clear_class_variable()
    # project closing tags
    project.closing_tags(iec60870_5_config)

    iec60870_5_config.close()
    k_bus.close()

    # Zipping POU folder
    shutil.make_archive(BASE_DIR + '\\POUs', 'zip', fl_pou_files)

    # Configuring .zip file
    with zipfile.ZipFile('configuration.zip', 'w') as zp:
        if os.path.isdir(fl_pou_files):
            zp.write(os.path.abspath("POUs.zip"), "/POUs.zip")
        if os.path.isfile(fl_iec60870_5_config):
            zp.write(fl_iec60870_5_config, "/iec60870_5_configuration.xml")
        if os.path.isfile(fl_k_bus):
            zp.write(fl_k_bus, "/k_bus_configuration.xml")
    zp.close()

    # Sending response
    return http_response('configuration.zip', 'rb')


def http_response(file, mode):
    # Sending response
    try:
        # Opened as bit stream in order to avoid encoding errors
        zip_file = open(file, mode)
        response = HttpResponse(zip_file, content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename=' + file
    except IOError:
        response = HttpResponseNotFound('<h1>File doesnt exist (Now you can start to panic)</h1>')

    return response
