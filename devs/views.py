import xml.etree.ElementTree as ET
import zipfile
from django.shortcuts import render
from devs.models import Device
from cards.models import Card
import os
from django.http import HttpResponse, HttpResponseNotFound
import datetime
from server import Server, ServerDevice
from project import Project
from kbus import Kbus
import kbus
from django.http import JsonResponse
import pou
import shutil

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Create your views here.
def configurator_view(request):
    devices = Device.objects.all()
    devices_num = devices.count()
    input_cards = Card.objects.filter(IO='DI').all()
    output_cards = Card.objects.filter(IO='DO').all()
    input_cards_num = input_cards.count()
    output_cards_num = output_cards.count()

    context = {
        "devices": devices,
        "devices_num": devices_num,
        "input_cards": input_cards,
        "output_cards": output_cards,
        "input_cards_num": input_cards_num,
        "output_cards_num": output_cards_num
    }

    return render(request, "configurator.html", context)


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
        center_ins = Server(center.attrib['name'], server_iteration, iec60870_5_config)
        center_ins.headers()
        for card in center.iter('card'):
            if card.attrib['server'] == 'yes':
                ServerDevice(card.text, 'card', int(card.attrib['number']), server_iteration, iec60870_5_config)
            if card.attrib['io'] == 'yes':
                kbus_ins = Kbus(card.text)
                kbus_ins.create_kbus(int(card.attrib['number']))
            pou.create_pous(card.text, int(card.attrib['number']), 'DO', server_iteration)
        for device in center.iter('device'):
            if device.attrib['server'] == 'yes':
                ServerDevice(device.text, 'device', int(device.attrib['number']), server_iteration, iec60870_5_config)
            # if device.attrib['client'] == 'yes':
            pou.create_pous(device.text, int(device.attrib['number']), device.attrib['operation'], server_iteration)
        server_iteration += 1
        # server closing tags
        center_ins.closing_tags()
    # Creating user-prg
    pou.create_user_prg()
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
