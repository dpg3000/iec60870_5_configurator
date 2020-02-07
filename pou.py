import os
import shutil
import support_functions
from server_parts.models import Obj35mMeTe
from devs.models import Device

path = os.path.dirname(os.path.abspath(__file__)) + '\\POUs'

# These lists were previously filled with the signal names in the server instance
# measurements
measurements_list = []
measurements_names_list = []
# states
states_list = []
states_names_list = []
# single commands
commands_list = []
commands_names_list = []
commands_triggers_list = []

# Execution time related lists
pou_instance_list = []
rtu_instance_list = []
device_list = []

# Data object repository for pou interface management
fbd_model = None
user_prg_model = None
device_model = None
rtu_model = None
pack_model = None
check_model = None
map_model = None
rise_model = None
save_model = None
sbo_model = None
handler_model = None


def delete_pous():
    folder = path
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def create_pou(device_name, device_quantity, device_operation, server_iteration):
    # Main purposes sequence list
    device_rtu_sequence = [(len(measurements_list[0]), 'measure'),
                           (len(states_list[0]), 'state'),
                           (len(commands_list[0]), 'command')]

    for rtu in device_rtu_sequence:
        if rtu[1] == 'command':
            pack3 = pack_model.pack(device_name, rtu[0], rtu[1], 'trigger', server_iteration, path)
            pou_instance_list.append(pack3)

        if rtu[1] == 'state':
            pack4 = pack_model.pack(device_name, rtu[0], rtu[1], 'trigger', server_iteration, path)
            rise0 = rise_model.rise(device_name, rtu[0], rtu[1], server_iteration, path)
            pou_instance_list.append(pack4)
            pou_instance_list.append(rise0)

        # Common ground between RTUs
        pack0 = pack_model.pack(device_name, rtu[0], rtu[1], 'values', server_iteration, path)
        check0 = check_model.check(device_name, rtu[0], rtu[1], server_iteration, path)
        map0 = map_model.map(device_name, rtu[0], rtu[1], server_iteration, path)
        pack1 = pack_model.pack(device_name, rtu[0], rtu[1], 'save', server_iteration, path)
        pack2 = pack_model.pack(device_name, rtu[0], rtu[1], 'label', server_iteration, path)
        save0 = save_model.save(device_name, rtu[0], rtu[1], server_iteration, path)

        # rtu instances
        pou_instance_list.append(pack0)
        pou_instance_list.append(check0)
        pou_instance_list.append(map0)
        pou_instance_list.append(pack1)
        pou_instance_list.append(pack2)
        pou_instance_list.append(save0)

        # SBO capabilities
        if device_operation == "SBO":
            if rtu[1] == 'command':
                if rtu[0] % 2:
                    return f"Error - Device: {device_name}. The list of commands in the database should be even to " \
                           f"use SBO "
                else:
                    sbo0 = sbo_model.sbo(device_name, rtu[0], rtu[1], server_iteration, path)
                    handler0 = handler_model.handler(device_name, server_iteration, path)
                    pou_instance_list.append(sbo0)
                    pou_instance_list.append(handler0)
        else:
            if rtu[1] == 'Command':
                if Device.objects.filter(Name=device_name).first().SBO:
                    if len(commands_list[0]) % 2:
                        return f"Error - Device: {device_name}. The list of commands in the database should be even " \
                               f"to allow DO/SBO compatibility "

        # rtu
        rtu = rtu_model.rtu(device_name, device_operation, rtu[0], rtu[1], pou_instance_list, server_iteration, path)
        rtu_instance_list.append(rtu)

        # After creating the rtu for previous purpose, clearing the instance related names
        pou_instance_list.clear()

    # Configuring device
    device0 = device_model.device(device_name, device_operation, rtu_instance_list, device_rtu_sequence, server_iteration, path)

    # Clearing rtu instance list for next device
    rtu_instance_list.clear()

    # Copying source lists to avoid reference related clearing
    measurements = measurements_list.copy()
    measurements_names = measurements_names_list.copy()
    states = states_list.copy()
    states_names = states_names_list.copy()
    commands = commands_list.copy()
    commands_names = commands_names_list
    commands_triggers = commands_triggers_list.copy()

    protocol = Device.objects.filter(Name=device_name).first().Protocol

    device_list.append(
        {
            'name': device0,
            'quantity': device_quantity,
            'operation': device_operation,
            'protocol': protocol,
            'measurements': measurements,
            'measurements_names': measurements_names,
            'states': states,
            'states_names': states_names,
            'commands': commands,
            'commands_names': commands_names,
            'commands_triggers': commands_triggers
        }
    )

    # Clearing lists related to a particular device to leave room for next device
    measurements_list.clear()
    measurements_names_list.clear()
    states_list.clear()
    states_names_list.clear()
    commands_list.clear()
    commands_names_list.clear()
    commands_triggers_list.clear()

    return False


def create_user_prg():
    # user_prg
    user_prg_model.user_prg()

    # clearing device list
    device_list.clear()






