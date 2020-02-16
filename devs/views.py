import xml.etree.ElementTree as ET
import zipfile
from django.shortcuts import render
from devs.models import Device
from cards.models import Card
import os
from django.http import HttpResponse, HttpResponseNotFound
import datetime
from server import Server, ServerDevice, device_ajax_request
from project import Project
from kbus import BusModule, assemble_modules
from django.http import JsonResponse
import pou
from pou import delete_pous
import shutil

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Create your views here.
def configurator_view(request):
    # Collecting the necessary information to render the form page
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
    # Obtaining data
    device_name = request.GET.get('device_name', None)

    # Client evaluation
    client_existence = Device.objects.filter(Name=device_name).first().ClientObjs
    if client_existence:
        client_existence = True
    else:
        client_existence = False

    # Getting operation data
    do_capability = Device.objects.filter(Name=device_name).first().DO
    sbo_capability = Device.objects.filter(Name=device_name).first().SBO

    # Getting server data
    device_data = device_ajax_request(device_name)

    data = {
        'is_client': client_existence,
        'is_do': do_capability,
        'is_sbo': sbo_capability,
        'device_data': device_data
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
    flag_input_cards = False
    flag_output_cards = False
    bus_modules_list = []
    delete_pous()
    for center in root.iter('center'):
        center_ins = Server(center.attrib['name'], server_iteration, iec60870_5_config)
        center_ins.headers()
        for input_card in center.iter('input-card'):
            if input_card.attrib['server'] == 'yes':
                ServerDevice(input_card.text, 'card', int(input_card.attrib['number']), server_iteration, iec60870_5_config)
                flag_input_cards = True
            if input_card.attrib['io'] == 'yes':
                for k in range(int(input_card.attrib['number'])):
                    kbus_ins = BusModule(input_card.text)
                    bus_modules_list.append(kbus_ins)
        for output_card in center.iter('output-card'):
            if output_card.attrib['server'] == 'yes':
                ServerDevice(output_card.text, 'card', int(output_card.attrib['number']), server_iteration, iec60870_5_config)
                flag_output_cards = True
            if output_card.attrib['io'] == 'yes':
                for k in range(int(output_card.attrib['number'])):
                    kbus_ins = BusModule(output_card.text)
                    bus_modules_list.append(kbus_ins)
        if flag_input_cards or flag_output_cards:
            pou.create_pous('Cards', 'card', 1, 'DO', server_iteration)
        for device in center.iter('device'):
            if device.attrib['server'] == 'yes':
                ServerDevice(device.text, 'device', int(device.attrib['number']), server_iteration, iec60870_5_config)
            # if device.attrib['client'] == 'yes':
            # GESTIONAR EL CLIENTE
            pou.create_pous(device.text, 'device', int(device.attrib['number']), device.attrib['operation'], server_iteration)
        server_iteration += 1
        # server closing tags
        center_ins.closing_tags()
    # Creating user-prg
    pou.create_user_prg()
    # write k-bus instances
    assemble_modules(bus_modules_list, k_bus)
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
