import os
import shutil
import support_functions
from server_parts.models import Obj35mMeTe
from devs.models import Device

path = os.path.dirname(os.path.abspath(__file__)) + '\\POUs'

# These lists were previously filled with the signal names in the server instance
measurements_list = []
states_list = []
single_commands_list = []
double_commands_list = []
iec_new_message_list = []

# Execution time related lists
rtu_pou_instance_list = []
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
    device_rtu_sequence = [(len(measurements_list[0]), 'measure'), (len(states_list[0]), 'state'), (len(single_commands_list[0]), 'command')]

    for rtu in device_rtu_sequence:
        if rtu[1] == 'command':
            pack3 = pack_model.pack(device_name, rtu[0], rtu[1], 'trigger', server_iteration, path)
            rtu_pou_instance_list.append(pack3)

        if rtu[1] == 'state':
            pack4 = pack_model.pack(device_name, rtu[0], rtu[1], 'trigger', server_iteration, path)
            rise0 = rise_model.rise(device_name, rtu[0], rtu[1], server_iteration, path)
            rtu_pou_instance_list.append(pack4)
            rtu_pou_instance_list.append(rise0)

        # Common ground between RTUs
        pack0 = pack_model.pack(device_name, rtu[0], rtu[1], 'values', server_iteration, path)
        check0 = check_model.check(device_name, rtu[0], rtu[1], server_iteration, path)
        map0 = map_model.map(device_name, rtu[0], rtu[1], server_iteration, path)
        pack1 = pack_model.pack(device_name, rtu[0], rtu[1], 'save', server_iteration, path)
        pack2 = pack_model.pack(device_name, rtu[0], rtu[1], 'label', server_iteration, path)
        save0 = save_model.save(device_name, rtu[0], rtu[1], server_iteration, path)

        # rtu instances
        rtu_pou_instance_list.append(pack0)
        rtu_pou_instance_list.append(check0)
        rtu_pou_instance_list.append(map0)
        rtu_pou_instance_list.append(pack1)
        rtu_pou_instance_list.append(pack2)
        rtu_pou_instance_list.append(save0)

        # SBO capabilities
        if device_operation == "SBO":
            if rtu[1] == 'command':
                control_list_len = 0
                if single_commands_list:
                    control_list_len += len(single_commands_list[0])
                if double_commands_list:
                    control_list_len += len(double_commands_list[0])
                if control_list_len % 2:
                    return f"Error - Device: {device_name}. The list of commands in the database should be even to " \
                           f"use SBO "
                else:
                    sbo0 = sbo_model.sbo(device_name, control_list_len, rtu[1], server_iteration, path)
                    handler0 = handler_model.handler(device_name, server_iteration, path)
                    rtu_pou_instance_list.append(sbo0)
                    rtu_pou_instance_list.append(handler0)
        else:
            if rtu[1] == 'Command':
                if Device.objects.filter(Name=device_name).first().SBO:
                    if len(single_commands_list[0]) % 2:
                        return f"Error - Device: {device_name}. The list of commands in the database should be even " \
                               f"to allow DO/SBO compatibility "

        # rtu
        rtu = rtu_model.rtu(device_name, device_operation, rtu[0], rtu[1], rtu_pou_instance_list, server_iteration, path)
        rtu_instance_list.append(rtu)

        # After creating the rtu for previous purpose, clearing the instance related names
        rtu_pou_instance_list.clear()

    # Copying source lists to avoid reference related clearing
    measurements = measurements_list.copy()
    states = states_list.copy()
    single_commands = single_commands_list.copy()
    double_commands = double_commands_list.copy()           # Not used for now
    iec_new_message = iec_new_message_list.copy()

    # Configuring device
    device0 = device_model.device(device_name, device_operation, rtu_instance_list, device_rtu_sequence, server_iteration, path)
    device_list.append(
        (
            device0,
            device_quantity,
            measurements,
            states,
            single_commands,
            device_operation,
            iec_new_message
        )
    )

    # Clearing lists related to a particular device to leave room for next device
    measurements_list.clear()
    states_list.clear()
    single_commands_list.clear()
    double_commands_list.clear()
    iec_new_message_list.clear()

    return False


def user_prg():
    # create file
    prg_ = open(path + "\\USER_PRG.EXP", "w+")

    # private headers
    prg_.write("""(* @NESTEDCOMMENTS := 'Yes' *)
                (* @PATH := '\/SGL_Sismored\/Sismored 4.0\/Imported' *)
                (* @OBJECTFLAGS := '0, 8' *)
                (* @SYMFILEFLAGS := '2048' *)""")
    prg_.write("\n")

    # variable definition
    # headers
    pou_name = "USER_PRG"
    headers = "PROGRAM " + pou_name + "\n"
    prg_.write(headers)

    # Internal variables
    prg_.write("VAR" + "\n")
    total_networks = 0
    for item in device_list:
        for i in range(item[1]):
            prg_.write("inst" + str(i) + item[0] + ": " + item[0] + ";" + "\n")
        total_networks += item[1]
    prg_.write("END_VAR" + "\n")

    # End definition
    prg_.write("(* @END_DECLARATION := '0' *)" + "\n")

    # FBD Code
    prg_.write("_FBD_BODY\n")
    prg_.write("_NETWORKS : {}\n".format(total_networks))

    # instantiation
    for item in device_list:
        _device_fbd(item, prg_)

    device_list.clear()

    # Final tag
    prg_.write("END_FUNCTION_BLOCK" + "\n")
    prg_.close()


def _device_fbd(device, file):
    for i in range(device[1]):
        file.write("""_NETWORK
            _COMMENT
            ''
            _END_COMMENT
            _ASSIGN
            _FUNCTIONBLOCK\n""")
        file.write("inst" + str(i) + device[0] + "\n")
        if device[5] == "SBO":
            file.write("_BOX_EXPR : " + str(len(device[2][i]) * 3 + len(device[3][i]) * 3 + len(device[4][i]) * 4 +
                                            int(len(device[4][i]) / 2) + 5) + "\n")
        else:
            file.write("_BOX_EXPR : " + str(len(device[2][i]) * 3 + len(device[3][i]) * 3 + len(device[4][i]) * 4 + 5) +
                       "\n")

        # Inputs
        file.write("""_OPERAND
                _EXPRESSION
                _POSITIV
                ???
                _OPERAND
                _EXPRESSION
                _POSITIV
                ???
                _OPERAND
                _EXPRESSION
                _POSITIV
                ???
                _OPERAND
                _EXPRESSION
                _POSITIV
                ???
                _OPERAND
                _EXPRESSION
                _POSITIV
                ???""" + "\n")

        # Input unit
        # Measurements
        for s in range(len(device[2][i])):
            file.write("""_OPERAND
                _EXPRESSION
                _POSITIV""" + "\n")
            file.write("???\n")

        for s in range(len(device[2][i])):
            file.write("""_OPERAND
                            _EXPRESSION
                            _POSITIV""" + "\n")
            file.write("FALSE\n")

        for signal in device[2][i]:
            file.write("""_OPERAND
                                        _EXPRESSION
                                        _POSITIV""" + "\n")
            name = signal.split("_")
            identification = ""
            try:
                if name[5]:
                    identification = name[2] + "_" + name[3]
            except:
                identification = name[2]

            file.write("'{}'\n".format(identification))

        # States
        for s in range(len(device[3][i])):
            file.write("""_OPERAND
                    _EXPRESSION
                    _POSITIV""" + "\n")
            file.write("???\n")

        for s in range(len(device[3][i])):
            file.write("""_OPERAND
                                _EXPRESSION
                                _POSITIV""" + "\n")
            file.write("TRUE\n")

        for signal in device[3][i]:
            file.write("""_OPERAND
                                            _EXPRESSION
                                            _POSITIV""" + "\n")
            name = signal.split("_")

            identification = ""
            try:
                if name[5]:
                    identification = name[2] + "_" + name[3]
            except:
                identification = name[2]

            file.write("'{}'\n".format(identification))

        # Commands
        for signal in device[4][i]:
            file.write("""_OPERAND
                    _EXPRESSION
                    _POSITIV""" + "\n")
            file.write("{}\n".format(signal))

        for s in range(len(device[4][i])):
            file.write("""_OPERAND
                                _EXPRESSION
                                _POSITIV""" + "\n")
            file.write("TRUE\n")

        for signal in device[4][i]:
            file.write("""_OPERAND
                                _EXPRESSION
                                _POSITIV""" + "\n")
            name = signal.split("_")
            identification = ""
            try:
                if name[5]:
                    identification = name[2] + "_" + name[3]
            except:
                identification = name[2]

            file.write("'{}'\n".format(identification))

        # iec new message triggers
        for trigger in device[6][i]:
            file.write("""_OPERAND
                                _EXPRESSION
                                _POSITIV""" + "\n")
            file.write(trigger + "\n")

        # Select And Execute
        if device[5] == 'SBO':
            for k in range(int(len(device[4][i]) / 2)):
                file.write("""_OPERAND
                                    _EXPRESSION
                                    _POSITIV
                                    ???""" + "\n")

        # Outputs
        file.write("""_EXPRESSION
            _POSITIV""" + "\n")
        file.write(device[0] + "\n")
        if device[5] == 'SBO':
            file.write("_OUTPUTS : " + str(len(device[2][i]) - 1 + len(device[3][i]) + 2 * len(device[4][i])) + "\n")
        else:
            file.write("_OUTPUTS : " + str(len(device[2][i]) - 1 + len(device[3][i]) + len(device[4][i])) + "\n")

        # Output unit
        # Measurements
        for s in range(len(device[2][i])):
            if s != 0:
                file.write("""_OUTPUT
                    _POSITIV
                    _NO_SET""" + "\n")
                file.write("{}\n".format(device[2][i][s]))

        # States
        for signal in device[3][i]:
            file.write("""_OUTPUT
                                _POSITIV
                                _NO_SET""" + "\n")
            file.write("{}\n".format(signal))

        # Commands
        for s in range(len(device[4][i])):
            file.write("""_OUTPUT
                    _POSITIV
                    _NO_SET""" + "\n")
            file.write("???\n")

        # Select And Execute
        if device[5] == 'SBO':
            for s in range(len(device[4][i])):
                file.write("""_OUTPUT
                                    _POSITIV
                                    _NO_SET""" + "\n")
                file.write("???\n")

        file.write("""_EXPRESSION
            _POSITIV
            _OUTPUTS : 1
            _OUTPUT
            _POSITIV
            _NO_SET""" + "\n")
        file.write(device[2][i][0] + "\n")






