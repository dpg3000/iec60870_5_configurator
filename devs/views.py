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
from django.contrib import messages
from django.shortcuts import redirect

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

    # Getting operation data
    do_capability = Device.objects.filter(Name=device_name).first().DO
    sbo_capability = Device.objects.filter(Name=device_name).first().SBO

    # Getting server data
    device_data = device_ajax_request(device_name)

    data = {
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

    # String to concatenate the processing error messages
    error_messages = ""

    # Initial erase to avoid partial overwriting
    if os.path.isfile(fl_iec60870_5_config):
        os.remove(fl_iec60870_5_config)

    if os.path.isfile(fl_k_bus):
        os.remove(fl_k_bus)

    # Open file to write (w+ -> if the file doesn't exist, it is created)
    iec60870_5_config = open("iec60870_5_configuration.xml", "w+")
    k_bus = open("k_bus_configuration.xml", "w+")

    # Project header with time stamp
    project = Project(datetime.datetime.now(), iec60870_5_config)
    project.headers()

    # Parsing xml from form data
    raw_xml = request.POST.get('request-data')
    root = ET.fromstring(raw_xml)

    # iterating over parsed xml to create the server instances
    server_iteration = 0
    flag_input_cards = False
    flag_output_cards = False
    flag_general_cards = True
    bus_modules_list = []
    delete_pous()

    # Centers
    for center in root.iter('center'):
        center_ins = Server(center.attrib['name'], server_iteration, iec60870_5_config)
        center_ins.headers()

        # Input cards
        for input_card in center.iter('input-card'):
            # Server
            if input_card.attrib['server'] == 'yes':
                server_input_car = ServerDevice(
                    name=input_card.text,
                    element='card',
                    quantity=int(input_card.attrib['number']),
                    server_iteration=server_iteration,
                    file=iec60870_5_config
                )
                error_message = server_input_car.create_device()
                if error_message:
                    messages.error(request, error_message)
                    error_messages += error_message + '\n'
                flag_input_cards = True
            # K-bus
            if input_card.attrib['io'] == 'yes':
                for k in range(int(input_card.attrib['number'])):
                    kbus_ins = BusModule(input_card.text)
                    bus_modules_list.append(kbus_ins)

        # Output cards
        for output_card in center.iter('output-card'):
            # Server
            if output_card.attrib['server'] == 'yes':
                server_output_card = ServerDevice(
                    name=output_card.text,
                    element='card',
                    quantity=int(output_card.attrib['number']),
                    server_iteration=server_iteration,
                    file=iec60870_5_config
                )
                error_message = server_output_card.create_device()
                if error_message:
                    messages.error(request, error_message)
                    error_messages += error_message + '\n'
                flag_output_cards = True
            # K-bus
            if output_card.attrib['io'] == 'yes':
                for k in range(int(output_card.attrib['number'])):
                    kbus_ins = BusModule(output_card.text)
                    bus_modules_list.append(kbus_ins)

        # POU device for cards
        if flag_input_cards or flag_output_cards:
            error_message = pou.create_pous(
                device_name='Cards',
                element='card',
                quantity=1,
                operation='DO',
                server_iteration=server_iteration
            )
            flag_input_cards = False
            flag_output_cards = False
            flag_general_cards = True
            if error_message:
                messages.error(request, error_message)
                error_messages += error_message + '\n'

        # Devices
        for device in center.iter('device'):
            # Server
            if device.attrib['server'] == 'yes':
                server_device = ServerDevice(
                    name=device.text,
                    element='device',
                    quantity=int(device.attrib['number']),
                    server_iteration=server_iteration,
                    file=iec60870_5_config
                )
                error_message = server_device.create_device()
                if error_message:
                    messages.error(request, error_message)
                    error_messages += error_message + '\n'
            # Client
            # if device.attrib['client'] == 'yes':
            # GESTIONAR EL CLIENTE
            pou.create_pous(
                device_name=device.text,
                element='device',
                quantity=int(device.attrib['number']),
                operation=device.attrib['operation'],
                server_iteration=server_iteration
            )

        # Increase server iteration
        server_iteration += 1
        # server closing tags
        center_ins.closing_tags()

    # Creating user-prg
    pou.create_user_prg()
    # write k-bus instances
    if flag_general_cards:
        assemble_modules(bus_modules_list, k_bus)
    # project closing tags
    project.closing_tags()

    # Closing files
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
    if error_messages:
        print(error_messages)
        return redirect('/configurator')
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
