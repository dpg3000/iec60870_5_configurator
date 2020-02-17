import os
import shutil
from devs.models import Device
import itertools

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
pou_list = []
rtu_instance_list = []
device_list = []

# sequence dictionary
sequence = {}

# Data object repository for pou interface management
fbd_model = None
user_prg_model = None
pack_loc_rem_model = None
check_loc_rem_model = None
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
            print(f"Failed to delete {file_path}. Reason: {e}")


def create_pous(device_name, element, device_quantity, operation, server_iteration):
    # Hub device/card
    protocol = ''
    if element == 'device':
        protocol = Device.objects.filter(Name=device_name).first().Protocol
    elif element == 'card':
        protocol = 'IO-Logic'
    else:
        return f"Error: unknown element in the device/card hub inside create_pous()"

    # Main purposes sequence list
    if measurements_list:
        if element == 'card':
            # Joining the inner devices (in this case cards) to collect them in a single device POU
            measurements_temp = list(itertools.chain(*measurements_list))
            measurements_list.clear()
            measurements_list.append(measurements_temp)
        sequence['measure'] = len(measurements_list[0])
    if states_list:
        if element == 'card':
            # Joining the inner devices (in this case cards) to collect them in a single device POU
            states_temp = list(itertools.chain(*states_list))
            states_list.clear()
            states_list.append(states_temp)
            states_names_temp = list(itertools.chain(*states_names_list))
            states_names_list.clear()
            states_names_list.append(states_names_temp)
        sequence['state'] = len(states_list[0])
    if commands_list:
        if element == 'card':
            # Joining the inner devices (in this case cards) to collect them in a single device POU
            commands_temp = list(itertools.chain(*commands_list))
            commands_list.clear()
            commands_list.append(commands_temp)
            commands_names_temp = list(itertools.chain(*commands_names_list))
            commands_names_list.clear()
            commands_names_list.append(commands_names_temp)
            commands_triggers_temp = list(itertools.chain(*commands_triggers_list))
            commands_triggers_list.clear()
            commands_triggers_list.append(commands_triggers_temp)
        sequence['command'] = len(commands_list[0])

    for purpose in sequence:
        if purpose == 'command':
            # Generating pou and related name
            pack3 = pack_model.pack(device_name, sequence[purpose], purpose, 'trigger', server_iteration, path)

            # Adding to rtu instance list
            pou_list.append(pack3)

        if purpose == 'state':
            # Generating pou and related name
            pack4 = pack_model.pack(device_name, sequence[purpose], purpose, 'trigger', server_iteration, path)
            rise0 = rise_model.rise(device_name, sequence[purpose], purpose, server_iteration, path)

            # Adding to rtu instance list
            pou_list.append(pack4)
            pou_list.append(rise0)

        # Common ground between RTUs
        # Generating pou and related name
        pack0 = pack_model.pack(device_name, sequence[purpose], purpose, 'values', server_iteration, path)
        check0 = check_model.check(device_name, sequence[purpose], purpose, server_iteration, path)
        map0 = map_model.map(device_name, sequence[purpose], purpose, server_iteration, path)
        pack1 = pack_model.pack(device_name, sequence[purpose], purpose, 'save', server_iteration, path)
        pack2 = pack_model.pack(device_name, sequence[purpose], purpose, 'label', server_iteration, path)
        save0 = save_model.save(device_name, sequence[purpose], purpose, server_iteration, path)

        # Adding to rtu instance list
        pou_list.append(pack0)
        pou_list.append(check0)
        pou_list.append(map0)
        pou_list.append(pack1)
        pou_list.append(pack2)
        pou_list.append(save0)

        # SBO capabilities
        if operation == "SBO":
            if purpose == 'command':
                if sequence[purpose] % 2:
                    return f"Error - Device: {device_name}. The list of commands in the database should be even to " \
                           f"use SBO "
                else:
                    # Generating pou and related name
                    sbo0 = sbo_model.sbo(device_name, sequence[purpose], purpose, server_iteration, path)
                    handler0 = handler_model.handler(device_name, server_iteration, path)

                    # Adding to rtu instance list
                    pou_list.append(sbo0)
                    pou_list.append(handler0)

        # rtu
        rtu = rtu_model.rtu(device_name, operation, sequence[purpose], purpose, pou_list, server_iteration, path)
        rtu_instance_list.append(rtu)

        # After creating the rtu for previous purpose, clearing the instance related names
        pou_list.clear()

    # Configuring device
    device0 = device_model.device(device_name, operation, rtu_instance_list, sequence, server_iteration, path)

    # Clearing rtu instance list for next device
    rtu_instance_list.clear()

    # Copying source lists to avoid reference related clearing
    measurements = measurements_list.copy()
    measurements_names = measurements_names_list.copy()
    states = states_list.copy()
    states_names = states_names_list.copy()
    commands = commands_list.copy()
    commands_names = commands_names_list.copy()
    commands_triggers = commands_triggers_list.copy()

    device_list.append(
        {
            'name':                 device0,
            'quantity':             device_quantity,
            'operation':            operation,
            'protocol':             protocol,
            'measurements':         measurements,
            'measurements_names':   measurements_names,
            'states':               states,
            'states_names':         states_names,
            'commands':             commands,
            'commands_names':       commands_names,
            'commands_triggers':    commands_triggers
        }
    )

    # Clearing lists related to a particular device to leave room for the next device
    measurements_list.clear()
    measurements_names_list.clear()
    states_list.clear()
    states_names_list.clear()
    commands_list.clear()
    commands_names_list.clear()
    commands_triggers_list.clear()

    # Clearing the sequence dictionary
    sequence.clear()

    return False


def create_user_prg():
    # Obtaining the total number of devices
    total_devices = 1
    for device in device_list:
        total_devices += device['quantity']

    # Pack local remote
    pack = pack_loc_rem_model.pack_loc_rem(total_devices, path)

    # Check local remote
    check = check_loc_rem_model.check_loc_rem(total_devices, path)

    # user_prg
    user_prg_model.user_prg(device_list, total_devices, pack, check, path)

    # clearing device list
    device_list.clear()
