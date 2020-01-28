import os
import shutil
import support_functions
from server_parts.models import Obj35mMeTe
from codesys.models import Map, Pack, Check, Save, Sbo, Rotate, Rtu, FbdTemplate, RiseToTrigger
from codesys.models import Device as Dev
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

data_type_dictionary = {
    'WORD': 'w',
    'BOOL': 'x',
    'SAVE': 'x',
    'NAME': 's',
    'STRING': 's',
    'BYTE': 'by'
}

output_dictionary = {
    'INPUT': 'aSignals',
    'SAVE': 'aSaves',
    'NAME': 'aNames'
}

purpose_dictionary = {
    'Measure': 'm',
    'State': 's',
    'Command': 'c'
}


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
    device_rtu_sequence = [
        ('word', len(measurements_list[0]), 'Measure'),
        ('bool', len(states_list[0]), 'State'),
        ('bool', len(single_commands_list[0]), 'Command')
    ]

    for rtu in device_rtu_sequence:
        if rtu[2] == 'Command':
            pack3 = _pack(device_name, rtu[0], rtu[1], rtu[2], 'packv0', server_iteration)
            rtu_pou_instance_list.append(pack3)

        if rtu[2] == 'State':
            pack4 = _pack(device_name, 'byte', rtu[1], rtu[2], 'packv0', server_iteration)
            rise0 = _rise(device_name, rtu[1], rtu[2], 'risev0', server_iteration)
            rtu_pou_instance_list.append(pack4)
            rtu_pou_instance_list.append(rise0)

        # Common ground between RTUs
        pack0 = _pack(device_name, rtu[0], rtu[1], rtu[2], 'packv0', server_iteration)
        check0 = _check(device_name, rtu[0], rtu[1], rtu[2], 'checkv0', server_iteration)
        map0 = _map(device_name, rtu[0], rtu[1], rtu[2], 'mapv0', server_iteration)
        pack1 = _pack(device_name, 'bool', rtu[1], rtu[2], 'packv0', server_iteration)
        pack2 = _pack(device_name, 'string', rtu[1], rtu[2], 'packv0', server_iteration)
        save0 = _save(device_name, rtu[0], rtu[1], rtu[2], 'savev0', server_iteration)

        # rtu instances
        rtu_pou_instance_list.append(map0)
        rtu_pou_instance_list.append(pack0)
        rtu_pou_instance_list.append(pack1)
        rtu_pou_instance_list.append(pack2)
        rtu_pou_instance_list.append(check0)
        rtu_pou_instance_list.append(save0)

        # SBO capabilities
        if device_operation == "SBO":
            if rtu[2] == 'Command':
                control_list_len = 0
                if single_commands_list:
                    control_list_len += len(single_commands_list[0])
                if double_commands_list:
                    control_list_len += len(double_commands_list[0])
                if control_list_len % 2:
                    return f"Error - Device: {device_name}. The list of commands in the database should be even to " \
                           f"use SBO "
                else:
                    sbo0 = _sbo(device_name, rtu[0], control_list_len, rtu[2], 'sbov0', server_iteration)
                    rtu_pou_instance_list.append(sbo0)
        else:
            if rtu[2] == 'Command':
                if Device.objects.filter(Name=device_name).first().SBO:
                    if len(single_commands_list[0]) % 2:
                        return f"Error - Device: {device_name}. The list of commands in the database should be even " \
                               f"to allow DO/SBO compatibility "

        # rtu
        rtu = _rtu(device_name, device_operation, rtu[0], rtu[1], rtu[2], rtu_pou_instance_list, 'rtuv0', server_iteration)
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
    device = _device(device_operation, device_name, device_rtu_sequence, rtu_instance_list, server_iteration)
    device_list.append(
        (
            device,
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


def _rise(device_name, num_objects, purpose, pou_version, server_iteration):
    # Obtain instance information
    declaration_info = RiseToTrigger.objects.filter(Version=pou_version).first().VariableDeclaration
    st_code_info = RiseToTrigger.objects.filter(Version=pou_version).first().Code

    # Instance data
    pou_name = "RiseToTrigger" + str(num_objects) + str(device_name) + purpose + str(server_iteration)

    # create file
    rise_object = open(path + "\\" + pou_name + ".EXP", "w+")

    # variable definition
    declaration_info = declaration_info.format(
        pou_name,
        num_objects,
        num_objects,
        num_objects
    )

    # ST code
    st_code_info = st_code_info.format(
        num_objects
    )

    rise_object.write(declaration_info + "\n" + st_code_info)

    # Closing file
    rise_object.close()

    return pou_name


def _map(device_name, data_type, num_objects, purpose, pou_version, server_iteration):
    # Obtain instance information
    declaration_info = Map.objects.filter(Version=pou_version).first().VariableDeclaration
    st_code_info = Map.objects.filter(Version=pou_version).first().Code

    # Instance data
    pou_name = "Map" + str(num_objects) + data_type + str(device_name) + purpose + str(server_iteration)

    # create file
    map_object = open(path + "\\" + pou_name + ".EXP", "w+")

    # Variable declaration
    # Inputs
    input_variable = Map.objects.filter(Version=pou_version).first().InputVariable
    input_str = support_functions.variable_to_declaration(
        data_type_dictionary[data_type.upper()] + input_variable,
        num_objects,
        data_type
    )

    # Outputs
    output_variable = Map.objects.filter(Version=pou_version).first().OutputVariable
    output_str = support_functions.variable_to_declaration(
        data_type_dictionary[data_type.upper()] + output_variable,
        num_objects,
        data_type
    )

    # Trigger and check declaration
    trigger_str = ""
    trigger_variable = ""
    check_str = ""
    check_variable = ""
    if purpose != 'Measure':
        trigger_variable = Map.objects.filter(Version=pou_version).first().TriggerVariable
        trigger_str = support_functions.variable_to_declaration('x' + trigger_variable, num_objects, data_type)
        check_variable = Map.objects.filter(Version=pou_version).first().CheckVariable
        check_str = support_functions.variable_to_declaration('x' + check_variable, num_objects, data_type)

    # Formatting declaration section
    declaration_info = declaration_info.format(
        pou_name,
        input_str,
        trigger_str,
        check_str,
        output_str
    )

    # ST Code block
    code = ""
    if purpose == 'Measure':
        for i in range(num_objects):
            code += f"{data_type_dictionary[data_type.upper()]}{output_variable}{i + 1} := " \
                    f"{data_type_dictionary[data_type.upper()]}{input_variable}{i + 1};\n"
    else:
        for i in range(num_objects):
            code += f"IF x{trigger_variable}{i + 1} OR x{check_variable}{i + 1} THEN\n " \
                    f"{data_type_dictionary[data_type.upper()]}{output_variable}{i + 1} := " \
                    f"{data_type_dictionary[data_type.upper()]}{input_variable}{i + 1};\n END_IF\n"

    # formatting code
    st_code_info = st_code_info.format(
        code
    )

    # formatting the main groups
    map_object.write(declaration_info + "\n" + st_code_info)

    # Closing file
    map_object.close()

    return pou_name


def _pack(device_name, data_type, num_objects, purpose, pou_version, server_iteration):
    # Obtain instance information
    declaration_info = Pack.objects.filter(Version=pou_version).first().VariableDeclaration
    st_code_info = Pack.objects.filter(Version=pou_version).first().Code

    # Instance data
    pou_name = "Pack" + str(num_objects) + data_type + str(device_name) + purpose + str(server_iteration)

    # create file
    pack_object = open(path + "\\" + pou_name + ".EXP", "w+")

    # variable definition
    # Inputs
    input_variable = Pack.objects.filter(Version=pou_version).first().InputVariable
    input_str = support_functions.variable_to_declaration(
        data_type_dictionary[data_type.upper()] + input_variable,
        num_objects,
        data_type
    )

    # Outputs
    output_variable = Pack.objects.filter(Version=pou_version).first().OutputVariable

    declaration_info = declaration_info.format(
        pou_name,
        input_str,
        output_variable, num_objects, data_type.upper()
    )

    # ST Code block
    code = ""
    for i in range(num_objects):
        code += f"{output_variable}[{i + 1}] := {data_type_dictionary[data_type.upper()]}{input_variable}{i + 1};\n"

    st_code_info = st_code_info.format(
        code
    )

    pack_object.write(declaration_info + "\n" + st_code_info)

    # closing file
    pack_object.close()

    return pou_name


def _check(device_name, data_type, num_objects, purpose, pou_version, server_iteration):
    # Obtain instance information
    declaration_info = Check.objects.filter(Version=pou_version).first().VariableDeclaration
    st_code_info = Check.objects.filter(Version=pou_version).first().Code

    # Instance data
    pou_name = "Check" + str(num_objects) + data_type + str(device_name) + purpose + str(server_iteration)

    # create file
    check_object = open(path + "\\" + pou_name + ".EXP", "w+")

    # variable definition
    declaration_info = declaration_info.format(
        pou_name,
        num_objects, data_type.upper(),
        num_objects,
        num_objects, data_type.upper()
    )

    # ST code
    st_code_info = st_code_info.format(
        num_objects
    )
    check_object.write(
        declaration_info +
        "\n" +
        st_code_info
    )

    # Closing file
    check_object.close()

    return pou_name


def _save(device_name, data_type, num_objects, purpose, pou_version, server_iteration):
    # Obtain instance information
    declaration_info = Save.objects.filter(Version=pou_version).first().VariableDeclaration
    st_code_info = Save.objects.filter(Version=pou_version).first().Code

    # Instance data
    pou_name = "Save" + str(num_objects) + data_type + str(device_name) + purpose + str(server_iteration)

    # create file
    save_object = open(path + "\\" + pou_name + ".EXP", "w+")

    # Variable definition
    # Inputs
    input_variable = Save.objects.filter(Version=pou_version).first().InputVariable

    # Internal variables
    iterator_variable = Save.objects.filter(Version=pou_version).first().IteratorVariable
    hysteresis_variable = Save.objects.filter(Version=pou_version).first().HysteresisVariable
    internal_input_variable = Save.objects.filter(Version=pou_version).first().InternalInputVariable

    # Obtaining hysteresis derivatives
    hysteresis = ""
    hysteresis_definition = ""
    hysteresis_condition = ""
    internal_input_definition = ""
    internal_input_code = ""
    hysteresis_code_end_tag = ""
    if data_type.upper() == "WORD":
        hysteresis = Obj35mMeTe.objects.filter(DeviceName=device_name).first().Hysteresis
    if hysteresis:
        hysteresis_definition = hysteresis_variable + f" : ARRAY[1..{num_objects}] OF INT := [{hysteresis}];"
        internal_input_definition = internal_input_variable + f" : ARRAY[1..{num_objects}] OF {data_type.upper()};"
        hysteresis_condition = f"IF ({input_variable}[{iterator_variable}] > ({internal_input_variable}" \
                               f"[{iterator_variable}] + (({hysteresis_variable}[{iterator_variable}] / 100) * " \
                               f"{internal_input_variable}[{iterator_variable}] ))) OR ({input_variable}" \
                               f"[{iterator_variable}] < ({internal_input_variable}[{iterator_variable}] - " \
                               f"(({hysteresis_variable}[{iterator_variable}] / 100) * {internal_input_variable}" \
                               f"[{iterator_variable}]))) THEN"
        internal_input_code = f"{internal_input_variable}[{iterator_variable}] := {input_variable}[{iterator_variable}];"
        hysteresis_code_end_tag = "END_IF"

    declaration_info = declaration_info.format(
        pou_name,
        input_variable, num_objects, data_type.upper(),
        num_objects,
        num_objects,
        num_objects,
        iterator_variable,
        hysteresis_definition,
        internal_input_definition
    )

    # ST Code block
    st_code_info = st_code_info.format(
        iterator_variable,
        iterator_variable,
        internal_input_code,
        data_type.upper(), input_variable, iterator_variable,
        iterator_variable, iterator_variable,
        iterator_variable,
        iterator_variable,
        hysteresis_condition,
        internal_input_code,
        data_type.upper(), input_variable, iterator_variable,
        iterator_variable, iterator_variable,
        hysteresis_code_end_tag,
        pou_name
    )

    # Write data stream
    save_object.write(declaration_info + "\n" + st_code_info)

    # Closing file
    save_object.close()

    return pou_name


def _sbo(device_name, data_type, num_objects, purpose, pou_version, server_iteration):
    # Obtain instance information
    declaration_info = Sbo.objects.filter(Version=pou_version).first().VariableDeclaration
    body_info = Sbo.objects.filter(Version=pou_version).first().Body
    core_info = Sbo.objects.filter(Version=pou_version).first().Core
    final_check_info = Sbo.objects.filter(Version=pou_version).first().FinalCheck

    # Instance data
    pou_name = "Sbo" + str(num_objects) + data_type + str(device_name) + purpose + str(server_iteration)

    # create file
    sbo_object = open(path + "\\" + pou_name + ".EXP", "w+")

    # Inputs
    input_variable = Sbo.objects.filter(Version=pou_version).first().InputVariable
    input_str = support_functions.variable_to_declaration(input_variable, num_objects)

    status_variable = Sbo.objects.filter(Version=pou_version).first().StatusVariable
    status_str = support_functions.variable_to_declaration(status_variable, num_objects / 2)

    # Outputs
    select_variable = Sbo.objects.filter(Version=pou_version).first().SelectVariable
    select_str = support_functions.variable_to_declaration(select_variable, num_objects / 2)

    execute_variable = Sbo.objects.filter(Version=pou_version).first().ExecuteVariable
    execute_str = support_functions.variable_to_declaration(execute_variable, num_objects / 2)

    # Internal variables
    internal_variable = Sbo.objects.filter(Version=pou_version).first().FlagVariable
    internal_str = support_functions.variable_to_declaration(internal_variable, num_objects / 2)

    declaration_info = declaration_info.format(
        pou_name,
        input_str,
        status_str,
        select_str,
        execute_str,
        internal_str
    )

    # ST Code block
    # COM state machine
    core_info_formatted = ""
    for s in range(int(num_objects / 2)):
        core_info_formatted += core_info.format(
            s + 1,
            (2 * s) + 1, (2 * s) + 2,
            s + 1,
            s + 1,
            s + 1,
            s + 1,
            s + 1,
            s + 1,
            s + 1,
            s + 1,
            s + 1,
            s + 1,
            s + 1,
            s + 1,
            s + 1,
            s + 1
        ) + "\n\n"

    # End jumper evaluation
    final_str = [internal_variable.format(i + 1) + " OR " for i in range(int(num_objects / 2))]
    final_str = ''.join(final_str)
    final_str = final_str[:-4]

    final_check_info = final_check_info.format(
        final_str
    )

    # Assemble body content
    core_info_formatted += final_check_info
    body_info = body_info.format(core_info_formatted)

    # Write data stream
    sbo_object.write(
        declaration_info +
        "\n" +
        body_info
    )

    sbo_object.close()

    return pou_name


def _rtu(device_name, device_operation, data_type, num_objects, purpose, instance_list, pou_version, server_iteration):
    # Obtain instance information
    declaration_info = Rtu.objects.filter(Version=pou_version).first().VariableDeclaration
    fbd_header_info = FbdTemplate.objects.first().Header

    # Instance data
    pou_name = "Rtu" + str(num_objects) + data_type + str(device_name) + purpose + str(server_iteration)

    # create file
    rtu_object = open(path + "\\" + pou_name + ".EXP", "w+")

    # variable definition
    # Inputs
    input_variable = Rtu.objects.filter(Version=pou_version).first().InputVariable
    input_str = support_functions.variable_to_declaration(
        data_type_dictionary[data_type.upper()] + input_variable,
        num_objects,
        data_type
    )

    save_variable = Rtu.objects.filter(Version=pou_version).first().SaveVariable
    save_str = support_functions.variable_to_declaration("x" + save_variable, num_objects)

    name_variable = Rtu.objects.filter(Version=pou_version).first().NameVariable
    name_str = support_functions.variable_to_declaration("s" + name_variable, num_objects)

    trigger_str = ""
    trigger_variable = ""
    if purpose != 'Measure':
        trigger_variable = Rtu.objects.filter(Version=pou_version).first().TriggerVariable
        trigger_str = support_functions.variable_to_declaration("x" + trigger_variable, num_objects, data_type)

    status_str = ""
    if device_operation == "SBO" and purpose == 'Command':
        status_variable = Rtu.objects.filter(Version=pou_version).first().StatusVariable
        status_str = support_functions.variable_to_declaration(status_variable, num_objects / 2, 'ENUM870_CLIENT_COMMAND')

    # Outputs
    output_variable = Rtu.objects.filter(Version=pou_version).first().OutputVariable
    output_str = support_functions.variable_to_declaration(
        data_type_dictionary[data_type.upper()] + output_variable,
        num_objects,
        data_type
    )

    select_str = ""
    execute_str = ""
    if device_operation == "SBO" and purpose == 'Command':
        select_variable = Rtu.objects.filter(Version=pou_version).first().SelectVariable
        select_str = support_functions.variable_to_declaration("x" + select_variable, num_objects / 2, data_type)

        execute_variable = Rtu.objects.filter(Version=pou_version).first().ExecuteVariable
        execute_str = support_functions.variable_to_declaration("x" + execute_variable, num_objects / 2, data_type)

    # Internal variables
    instance_block = ""
    for item in instance_list:
        if 'Save' not in item:
            instance_block += f"inst0{item} : {item};\n"

    sbo_error_str = ""
    if device_operation == "SBO" and purpose == 'Command':
        sbo_error_variable = Rtu.objects.filter(Version=pou_version).first().SBOErrorVariable
        sbo_error_str = f"e{sbo_error_variable} : eErrorCodes\n"

    declaration_info = declaration_info.format(
        pou_name,
        input_str,
        save_str,
        name_str,
        trigger_str,
        status_str,
        output_str,
        select_str,
        execute_str,
        instance_block,
        num_objects, data_type.upper(),
        num_objects,
        num_objects,
        num_objects,
        sbo_error_str
    )

    rtu_object.write(declaration_info + "\n")

    # FBD Code
    # Select body networks
    if purpose == 'Measure':
        body_networks = 6
    else:
        if purpose == 'Command' and device_operation == 'SBO':
            body_networks = 7
        else:
            body_networks = 8

    fbd_header_info = fbd_header_info.format(str(body_networks) + "\n")
    rtu_object.write(fbd_header_info)

    # RTU hub
    if purpose == 'Command':
        _pack_fbd(instance_list[0], num_objects, 'bool', trigger_variable, rtu_object)
        _pack_fbd(instance_list[1], num_objects, data_type, input_variable, rtu_object)
        _check_fbd(instance_list[2], 'aSignals', rtu_object)
        _map_fbd(instance_list[3], num_objects, data_type, purpose, rtu_object)
        _pack_fbd(instance_list[4], num_objects, 'bool', save_variable, rtu_object)
        _pack_fbd(instance_list[5], num_objects, 'string', name_variable, rtu_object)
        # _save_fbd(instance_list[6], num_objects, pack_out_0, pack_out_2, check_out_0[0], pack_out_1, check_out_0[1], rtu_object)
        # if device_operation == "SBO"
        #     _sbo_fbd(instance_list[7], num_objects, 'SBO', check_out_0[0], rtu_object)

    # Final tag
    rtu_object.write("END_FUNCTION_BLOCK" + "\n")
    rtu_object.close()

    return pou_name


def _map_fbd(item, num_objects, case, purpose, file):
    fbd_input_header_info = FbdTemplate.objects.first().InputHeader
    fbd_input_unit_info = FbdTemplate.objects.first().InputUnit
    fbd_output_header_info = FbdTemplate.objects.first().OutputHeader
    fbd_output_unit_info = FbdTemplate.objects.first().OutputUnit

    if purpose == 'c':
        box_expressions = 2 * num_objects
    else:
        box_expressions = num_objects

    fbd_input_header_info = fbd_input_header_info.format(
        item[0] + item[1],
        str(box_expressions + 3)
    )

    # Input unit
    fbd_input_unit_info_formatted = ""

    fbd_input_unit_info_formatted += fbd_input_unit_info.format("xFirstCycle\n")
    fbd_input_unit_info_formatted += fbd_input_unit_info.format("eAction\n")
    fbd_input_unit_info_formatted += fbd_input_unit_info.format("eState\n")

    for i in range(num_objects):
        instruction = input_dictionary[case.upper()] + "Input{}".format(i + 1) + "\n"
        fbd_input_unit_info_formatted += fbd_input_unit_info.format(
            instruction + "\n"
        )

    if purpose == 'c':
        for i in range(num_objects):
            instruction = input_dictionary[case.upper()] + "Trigger{}".format(i + 1) + "\n"
            fbd_input_unit_info_formatted += fbd_input_unit_info.format(
                instruction + "\n"
            )

    # Output header 1
    fbd_output_header_info_1 = fbd_output_header_info.format(
        item[1],
        str(num_objects - 1)
    )

    # Output unit 1
    fbd_output_unit_info_1 = ""
    for i in range(num_objects - 1):
        fbd_output_unit_info_1 += fbd_output_unit_info.format(
            input_dictionary[case.upper()] + "Output{}".format(i + 2) + "\n"
        )

    # Output header 2
    fbd_output_header_info_2 = fbd_output_header_info.format(
        "",
        str(1)
    )

    # Output unit 2
    fbd_output_unit_info_2 = fbd_output_unit_info.format(
        input_dictionary[case.upper()] + "Output1" + "\n"
    )

    file.write(
        fbd_input_header_info + "\n" +
        fbd_input_unit_info_formatted + "\n" +
        fbd_output_header_info_1 + "\n" +
        fbd_output_unit_info_1 + "\n" +
        fbd_output_header_info_2 + "\n" +
        fbd_output_unit_info_2
    )


def _pack_fbd(item, num_objects, case, signal, file):
    fbd_input_header_info = FbdTemplate.objects.first().InputHeader
    fbd_input_unit_info = FbdTemplate.objects.first().InputUnit
    fbd_output_header_info = FbdTemplate.objects.first().OutputHeader
    fbd_output_unit_info = FbdTemplate.objects.first().OutputUnit

    # Input header
    fbd_input_header_info = fbd_input_header_info.format(
        item[0] + item[1],
        str(num_objects)
    )

    # Input unit
    fbd_input_unit_info_formatted = ""
    for i in range(num_objects):
        signal_name = input_dictionary[case.upper()] + signal + "{}".format(i + 1)
        fbd_input_unit_info_formatted += fbd_input_unit_info.format(
            signal_name + "\n"
        )

    # Output header 1
    fbd_output_header_info_1 = fbd_output_header_info.format(
        item[1],
        str(0)
    )

    # Output header 2
    fbd_output_header_info_2 = fbd_output_header_info.format(
        "",
        str(1)
    )

    # Output unit
    fbd_output_unit_info = fbd_output_unit_info.format(
        output_dictionary[signal.upper()] + "\n"
    )

    file.write(
        fbd_input_header_info + "\n" +
        fbd_input_unit_info_formatted + "\n" +
        fbd_output_header_info_1 + "\n" +
        fbd_output_header_info_2 + "\n" +
        fbd_output_unit_info
    )


def _check_fbd(item, to_check, file):
    file.write("""_NETWORK
_COMMENT
''
_END_COMMENT
_ASSIGN
_FUNCTIONBLOCK\n""")
    file.write(item[0] + item[1] + "\n")
    file.write("_BOX_EXPR : 1\n")

    # input unit
    file.write("""_OPERAND
_EXPRESSION
_POSITIV""" + "\n")
    file.write(to_check + "\n")

    file.write("""_EXPRESSION
_POSITIV""" + "\n")
    file.write(item[1] + "\n")
    file.write("_OUTPUTS : 1\n")

    # output unit
    file.write("""_OUTPUT
_POSITIV
_NO_SET""" + "\n")
    file.write("sTime" + "\n")

    file.write("""_EXPRESSION
_POSITIV
_OUTPUTS : 1
_OUTPUT
_POSITIV
_NO_SET""" + "\n")
    file.write("aMaskChanges" + "\n")

    return "aMaskChanges", "sTime"


def _save_fbd(item, num_objects, signals, names, changes, saves, time, file):
    file.write("""_NETWORK

_COMMENT
''
_END_COMMENT
_FUNCTION""" + "\n")
    file.write("_BOX_EXPR : 9\n")
    file.write("""_OPERAND
_EXPRESSION
_POSITIV
xFirstCycle
_OPERAND
_EXPRESSION
_POSITIV
iSequenceOrder
_OPERAND
_EXPRESSION
_POSITIV""" + "\n")
    file.write(str(num_objects) + "\n")
    file.write("""_OPERAND
_EXPRESSION
_POSITIV
sProtocol""" + "\n")

    input_line = ""
    input_line += """_OPERAND
_EXPRESSION
_POSITIV
{}\n""".format(time)
    input_line += """_OPERAND
_EXPRESSION
_POSITIV
{}\n""".format(signals)
    input_line += """_OPERAND
_EXPRESSION
_POSITIV
{}\n""".format(names)
    input_line += """_OPERAND
_EXPRESSION
_POSITIV
{}\n""".format(changes)
    input_line += """_OPERAND
_EXPRESSION
_POSITIV
{}\n""".format(saves)
    input_line += """_EXPRESSION
_POSITIV
{}\n""".format(item[1])

    file.write(input_line)


def _sbo_fbd(instance, num_objects, step, signal, file):
    file.write("""_NETWORK
{}
_COMMENT
''
_END_COMMENT
_ASSIGN
_FUNCTIONBLOCK
{}
_BOX_EXPR : {}\n""".format(step, instance[0] + instance[1], num_objects + int(num_objects / 2) + 1))

    # inputs
    file.write("""_OPERAND
_EXPRESSION
_POSITIV
eState\n""")
    for i in range(num_objects):
        file.write("""_OPERAND
_EXPRESSION
_POSITIV
{}\n""".format(signal + "[" + str(i + 1) + "]"))
    for i in range(int(num_objects / 2)):
        file.write("""_OPERAND
_EXPRESSION
_POSITIV
{}\n""".format("Status" + str(i + 1)))

    # outputs
    file.write("""_EXPRESSION
_POSITIV
{}
_OUTPUTS : {}\n""".format(instance[1], (num_objects - 1) + 3))
    for i in range(int(num_objects / 2) - 1):
        file.write("""_OUTPUT
_POSITIV
_NO_SET
{}\n""".format("xSelect" + str(i + 2)))
    for i in range(int(num_objects / 2)):
        file.write("""_OUTPUT
_POSITIV
_NO_SET
{}\n""".format("xExecute" + str(i + 1)))

    file.write("""_OUTPUT
_POSITIV
_NO_SET
eErrorStatusOutput
_OUTPUT
_POSITIV
_NO_SET
xJumpRetry
_OUTPUT
_POSITIV
_NO_SET
xJumpSelectAndExecute\n""")

    file.write("""_EXPRESSION
_POSITIV
_OUTPUTS : 1
_OUTPUT
_POSITIV
_NO_SET
xSelect1\n""")


def _device(device_operation, device_name, io_sequence, rtu_instance_list, server_iteration):
    # Obtain instance information
    declaration_info = Dev.objects.filter(Version="devicev0").first().VariableDeclaration
    fbd_header_info = FbdTemplate.objects.first().Header

    # Meta-data
    pou_name = "Dev" + str(device_name) + str(server_iteration)

    # create file
    device_ = open(path + "\\" + pou_name + ".EXP", "w+")

    # variable definition
    # headers
    headers = "FUNCTION_BLOCK " + pou_name + "\n"
    device_.write(headers)

    # inputs
    device_.write("VAR_INPUT" + "\n")
    device_.write("xFirstCycle        :   BOOL;" + "\n")
    device_.write("iSequenceOrder     :   INT;" + "\n")
    device_.write("sProtocol          :   STRING;" + "\n")
    device_.write("eState             :   eStates;" + "\n")
    device_.write("eAction            :   eActions;" + "\n")
    for item in io_sequence:
        input_str = [input_dictionary[item[2].upper()] + item[0] + "{}, ".format(i + 1) for i in range(item[1])]
        input_str = ''.join(input_str)
        input_str = input_str[:-2]
        input_str += ": " + item[2].upper() + ";" + "\n"
        device_.write(input_str)

        input_str = ['xSave' + item[0] + "{}, ".format(i + 1) for i in range(item[1])]
        input_str = ''.join(input_str)
        input_str = input_str[:-2]
        input_str += ": BOOL;" + "\n"
        device_.write(input_str)

        input_str = ['sName' + item[0] + "{}, ".format(i + 1) for i in range(item[1])]
        input_str = ''.join(input_str)
        input_str = input_str[:-2]
        input_str += ": STRING;" + "\n"
        device_.write(input_str)

        if item[0] == "Command":
            input_str = ['xTrigger' + item[0] + "{}, ".format(i + 1) for i in range(item[1])]
            input_str = ''.join(input_str)
            input_str = input_str[:-2]
            input_str += ": BOOL;" + "\n"
            device_.write(input_str)

        if device_operation == "SBO" and item[0] == "Command":
            input_str = ["Status{}, ".format(i + 1) for i in range(int(item[1] / 2))]
            input_str = ''.join(input_str)
            input_str = input_str[:-2]
            input_str += ": ENUM870_CLIENT_COMMAND;" + "\n"
            device_.write(input_str)

    device_.write("END_VAR" + "\n")

    # Outputs
    device_.write("VAR_OUTPUT" + "\n")
    for item in io_sequence:
        output_str = [input_dictionary[item[2].upper()] + item[0] + "Output" + "{}, ".format(i + 1) for i in
                      range(item[1])]
        output_str = ''.join(output_str)
        output_str = output_str[:-2]
        output_str += ": " + item[2].upper() + ";" + "\n"
        device_.write(output_str)

        if device_operation == "SBO" and item[0] == "Command":
            output_str = ["Select{}, ".format(i + 1) for i in range(int(item[1] / 2))]
            output_str = ''.join(output_str)
            output_str = output_str[:-2]
            output_str += ": BOOL;" + "\n"
            device_.write(output_str)

            output_str = ["Execute{}, ".format(i + 1) for i in range(int(item[1] / 2))]
            output_str = ''.join(output_str)
            output_str = output_str[:-2]
            output_str += ": BOOL;" + "\n"
            device_.write(output_str)

    device_.write("END_VAR" + "\n")

    # Internal variables
    device_.write("VAR" + "\n")
    internal_line = ""
    for item in rtu_instance_list:
        internal_line += item[0] + item[1] + " : " + item[1] + ";" + "\n"
    device_.write(internal_line)
    device_.write("END_VAR" + "\n")

    # End definition
    device_.write("(* @END_DECLARATION := '0' *)" + "\n")

    # FBD Code block
    device_.write("_FBD_BODY\n")
    device_.write("_NETWORKS : " + str(len(rtu_instance_list)) + "\n")

    # Instantiation
    for i in range(len(rtu_instance_list)):
        _rtu_fbd(device_operation, rtu_instance_list[i], io_sequence[i], device_)

    # Final tag
    device_.write("END_FUNCTION_BLOCK" + "\n")
    device_.close()

    return pou_name


def _rtu_fbd(device_operation, item, io_sequence, file):
    file.write("""_NETWORK
    _COMMENT
    ''
    _END_COMMENT
    _ASSIGN
    _FUNCTIONBLOCK\n""")
    file.write(item[0] + item[1] + "\n")

    if io_sequence[0] == 'Command':
        if device_operation == 'SBO':
            file.write("_BOX_EXPR : " + str((io_sequence[1] * 4) + int(io_sequence[1] / 2) + 5) + "\n")
        else:
            file.write("_BOX_EXPR : " + str((io_sequence[1] * 4) + 5) + "\n")
    else:
        file.write("_BOX_EXPR : " + str((io_sequence[1] * 3) + 5) + "\n")

    # Inputs
    file.write("""_OPERAND
        _EXPRESSION
        _POSITIV
        xFirstCycle
        _OPERAND
        _EXPRESSION
        _POSITIV
        iSequenceOrder
        _OPERAND
        _EXPRESSION
        _POSITIV
        sProtocol
        _OPERAND
        _EXPRESSION
        _POSITIV
        eState
        _OPERAND
        _EXPRESSION
        _POSITIV
        eAction""" + "\n")
    # Input unit
    for i in range(io_sequence[1]):
        file.write("""_OPERAND
    _EXPRESSION
    _POSITIV""" + "\n")
        file.write(input_dictionary[io_sequence[2].upper()] + io_sequence[0] + "{}".format(i + 1) + "\n")
    for i in range(io_sequence[1]):
        file.write("""_OPERAND
    _EXPRESSION
    _POSITIV""" + "\n")
        file.write("xSave" + io_sequence[0] + "{}".format(i + 1) + "\n")
    for i in range(io_sequence[1]):
        file.write("""_OPERAND
    _EXPRESSION
    _POSITIV""" + "\n")
        file.write("sName" + io_sequence[0] + "{}".format(i + 1) + "\n")

    # New IEC message trigger
    if io_sequence[0] == 'Command':
        for i in range(io_sequence[1]):
            file.write("""_OPERAND
                _EXPRESSION
                _POSITIV""" + "\n")
            file.write("xTrigger" + io_sequence[0] + "{}".format(i + 1) + "\n")

    # SBO status
    if device_operation == 'SBO' and io_sequence[0] == 'Command':
        for i in range(int(io_sequence[1] / 2)):
            file.write("""_OPERAND
                _EXPRESSION
                _POSITIV""" + "\n")
            file.write("Status{}".format(i + 1) + "\n")

    file.write("""_EXPRESSION
    _POSITIV""" + "\n")
    file.write(item[1] + "\n")

    if device_operation == 'SBO' and io_sequence[0] == 'Command':
        file.write("_OUTPUTS : " + str((io_sequence[1] - 1) + io_sequence[1]) + "\n")
    else:
        file.write("_OUTPUTS : " + str(io_sequence[1] - 1) + "\n")

    # Output unit
    for i in range(io_sequence[1] - 1):
        file.write("""_OUTPUT
    _POSITIV
    _NO_SET""" + "\n")
        file.write(input_dictionary[io_sequence[2].upper()] + io_sequence[0] + "Output{}".format(i + 2) + "\n")

    if device_operation == 'SBO' and io_sequence[0] == 'Command':
        for i in range(int(io_sequence[1] / 2)):
            file.write("""_OUTPUT
                _POSITIV
                _NO_SET""" + "\n")
            file.write("Select{}".format(i + 1) + "\n")
        for i in range(int(io_sequence[1] / 2)):
            file.write("""_OUTPUT
                _POSITIV
                _NO_SET""" + "\n")
            file.write("Execute{}".format(i + 1) + "\n")

    file.write("""_EXPRESSION
    _POSITIV
    _OUTPUTS : 1
    _OUTPUT
    _POSITIV
    _NO_SET""" + "\n")
    file.write(input_dictionary[io_sequence[2].upper()] + io_sequence[0] + "Output1" + "\n")


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

