import os
import shutil
from server_parts.models import Obj35mMeTe
from codesys.models import Map, Pack, Check, Save, Sbo, Rotate, Rtu, FbdTemplate
from codesys.models import Device as Dev
from devs.models import Device

# These lists were previously filled with the signal names in the server instance
measurements_list = []
states_list = []
single_commands_list = []
double_commands_list = []

device_list = []

path = os.path.dirname(os.path.abspath(__file__)) + '\\POUs'

input_dictionary = {
    'WORD': 'w',
    'BOOL': 'x',
    'SAVE': 'x',
    'NAME': 's',
    'STRING': 's',
}
output_dictionary = {
    'INPUT': 'aSignals',
    'SAVE': 'aSaves',
    'NAME': 'aNames'
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
    device_rtu_sequence = [('word', len(measurements_list[0]), 'm'),
                           ('bool', len(states_list[0]), 's'),
                           ('bool', len(single_commands_list[0]), 'c')]
    rtu_instance_list = []
    instance_list = []
    for rtu in device_rtu_sequence:
        # model generation
        map0 = _map(device_name, rtu[0], rtu[1], rtu[2], server_iteration)
        pack0 = _pack(device_name, rtu[0], rtu[1], rtu[2], server_iteration)
        pack1 = _pack(device_name, 'bool', rtu[1], rtu[2], server_iteration)
        pack2 = _pack(device_name, 'string', rtu[1], rtu[2], server_iteration)
        check0 = _check(device_name, rtu[0], rtu[1], rtu[2], server_iteration)
        save0 = _save(device_name, rtu[0], rtu[1], rtu[2], server_iteration)

        # rtu instances
        instance_list.append(('inst0', map0))
        instance_list.append(('inst0', pack0))
        instance_list.append(('inst0', pack1))
        instance_list.append(('inst0', pack2))
        instance_list.append(('inst0', check0))
        instance_list.append(('inst0', save0))

        # SBO capabilities
        if device_operation == "SBO":
            if rtu[2] == 'c':
                control_list_len = 0
                if single_commands_list:
                    control_list_len += len(single_commands_list[0])
                if double_commands_list:
                    control_list_len += len(double_commands_list[0])
                if control_list_len % 2:
                    return "Error - Device: " + device_name + ". The list of commands in the database should be even " \
                                                              "to use SBO "
                sbo0 = _sbo(device_name, rtu[0], control_list_len, rtu[2], server_iteration)
                instance_list.append(('inst0', sbo0))
        else:
            if rtu[2] == 'c':
                if Device.objects.filter(Name=device_name).first().SBO:
                    if len(single_commands_list[0]) % 2:
                        return "Error - Device: " + device_name + ". The list of commands in the database should be " \
                                                                  "even to allow DO/SBO compatibility "

        # Rotate capabilities (103 protocol data frame contain useless metadata)
        if Device.objects.filter(Name=device_name).first().Protocol == "103":
            if rtu[2] == 'm':
                _rotate(device_name, rtu[0], rtu[1], rtu[2], server_iteration)

        # rtu
        rtu0 = _rtu(device_name, device_operation, rtu[0], rtu[1], rtu[2], instance_list, server_iteration)
        rtu_instance_list.append(('inst0', rtu0))

        # After creating the rtu for previous purpose, clearing the instance related names
        instance_list.clear()

    # shaping the device from previous rtus
    io_sequence = [('Measure', len(measurements_list[0]), 'word'),
                   ('State', len(states_list[0]), 'bool'),
                   ('Command', len(single_commands_list[0]), 'bool')]

    measurements = measurements_list.copy()
    states = states_list.copy()
    commands = single_commands_list.copy()

    device_list.append(
        (_device(device_operation, device_name, io_sequence, rtu_instance_list, server_iteration), device_quantity,
         measurements, states, commands, device_operation)
    )

    # Clearing lists related to a particular device to leave room for next device
    measurements_list.clear()
    states_list.clear()
    single_commands_list.clear()
    double_commands_list.clear()

    return False


def _rotate(device_name, data_type, num_objects, purpose, server_iteration):
    # Obtain instance information
    declaration_info = Rotate.objects.filter(Version="rotatev0").first().VariableDeclaration
    st_code_info = Rotate.objects.filter(Version="rotatev0").first().Code

    # Meta-data
    pou_name = "Rotate" + str(num_objects) + data_type + str(device_name) + purpose + str(server_iteration)

    # create file
    rotate_ = open(path + "\\" + pou_name + ".EXP", "w+")

    # variable definition
    # inputs
    input_str = ["wInput{}, ".format(i + 1) for i in range(num_objects)]
    input_str = ''.join(input_str)
    input_str = input_str[:-2]

    # outputs
    output_str = ["wOutput{}, ".format(i + 1) for i in range(num_objects)]
    output_str = ''.join(output_str)
    output_str = output_str[:-2]

    declaration_info = declaration_info.format(
        pou_name,
        input_str,
        output_str
    )

    # ST Code block
    internal_code = ""
    default_code = ""
    for i in range(num_objects):
        internal_code += ("wOutput{} := SHR(wInput{}, iNumberOfRotations);\n".format(i + 1, i + 1))
    for i in range(num_objects):
        default_code += ("wOutput{} := SHL(wInput{}, iNumberOfRotations);\n".format(i + 1, i + 1))

    st_code_info = st_code_info.format(
        internal_code,
        default_code
    )

    rotate_.write(
        declaration_info +
        "\n" +
        st_code_info
    )

    rotate_.close()

    return pou_name


def _map(device_name, data_type, num_objects, purpose, server_iteration):
    # Obtain instance information
    declaration_info = Map.objects.filter(Version="mapv0").first().VariableDeclaration
    st_code_info = Map.objects.filter(Version="mapv0").first().Code

    # Meta-data
    pou_name = "Map" + str(num_objects) + data_type + str(device_name) + purpose + str(server_iteration)

    # create file
    map_ = open(path + "\\" + pou_name + ".EXP", "w+")

    # variable definition
    # Inputs
    input_str = [input_dictionary[data_type.upper()] + "Input{}, ".format(i + 1) for i in range(num_objects)]
    input_str = ''.join(input_str)
    input_str = input_str[:-2]
    input_str += ": " + data_type.upper() + ";"

    # Input triggers
    trigger_str = ""
    if purpose == 'c':
        trigger_str = ["xTrigger{}, ".format(i + 1) for i in range(num_objects)]
        trigger_str = ''.join(trigger_str)
        trigger_str = trigger_str[:-2]
        trigger_str += ": " + data_type.upper() + ";"

    # Outputs
    output_str = [input_dictionary[data_type.upper()] + "Output{}, ".format(i + 1) for i in range(num_objects)]
    output_str = ''.join(output_str)
    output_str = output_str[:-2]
    output_str += ": " + data_type.upper() + ";"

    declaration_info = declaration_info.format(
        pou_name,
        input_str,
        trigger_str,
        output_str
    )

    # ST Code block
    code = ""
    for i in range(num_objects):
        if purpose == 'c':
            code += "IF xTrigger{} ".format(i + 1) + "THEN\n"
            code += input_dictionary[data_type.upper()] + "Output{} := ".format(i + 1) + \
                    input_dictionary[data_type.upper()] + "Input{};\n".format(i + 1)
            code += "END_IF\n"
        else:
            code += input_dictionary[data_type.upper()] + "Output{} := ".format(i + 1) + \
                    input_dictionary[data_type.upper()] + "Input{};\n".format(i + 1)

    st_code_info = st_code_info.format(
        code
    )

    map_.write(
        declaration_info +
        "\n" +
        st_code_info
    )

    # Closing file
    map_.close()

    return pou_name


def _pack(device_name, data_type, num_objects, purpose, server_iteration):
    # Obtain instance information
    declaration_info = Pack.objects.filter(Version="packv0").first().VariableDeclaration
    st_code_info = Pack.objects.filter(Version="packv0").first().Code

    # Meta-data
    pou_name = "Pack" + str(num_objects) + data_type + str(device_name) + purpose + str(server_iteration)

    # create file
    pack_ = open(path + "\\" + pou_name + ".EXP", "w+")

    # variable definition
    # Inputs
    input_str = [input_dictionary[data_type.upper()] + "Input{}, ".format(i + 1) for i in range(num_objects)]
    input_str = ''.join(input_str)
    input_str = input_str[:-2]
    input_str += ": " + data_type.upper() + ";"

    declaration_info = declaration_info.format(
        pou_name,
        input_str,
        num_objects, data_type.upper()
    )

    # ST Code block
    code = ""
    for i in range(num_objects):
        code += "aOutput[{}] := ".format(i + 1) + input_dictionary[data_type.upper()] + "Input{};\n".format(i + 1)

    st_code_info = st_code_info.format(
        code
    )

    pack_.write(
        declaration_info +
        "\n" +
        st_code_info
    )

    # closing file
    pack_.close()

    return pou_name


def _check(device_name, data_type, num_objects, purpose, server_iteration):
    # Obtain instance information
    declaration_info = Check.objects.filter(Version="checkv0").first().VariableDeclaration
    st_code_info = Check.objects.filter(Version="checkv0").first().Code

    # Meta-data
    pou_name = "Check" + str(num_objects) + data_type + str(device_name) + purpose + str(server_iteration)

    # create file
    check_ = open(path + "\\" + pou_name + ".EXP", "w+")

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
    check_.write(
        declaration_info +
        "\n" +
        st_code_info
    )

    # Closing file
    check_.close()

    return pou_name


def _save(device_name, data_type, num_objects, purpose, server_iteration):
    # Obtain instance information
    declaration_info = Save.objects.filter(Version="savev0").first().VariableDeclaration
    st_code_info = Save.objects.filter(Version="savev0").first().Code

    # Meta-data
    pou_name = "Save" + str(num_objects) + data_type + str(device_name) + purpose + str(server_iteration)

    # create file
    save_ = open(path + "\\" + pou_name + ".EXP", "w+")

    # Obtaining hysteresis derivatives
    hysteresis = ""
    hysteresis_definition = ""
    hyst_cdtn = ""
    last_values_array_definition = ""
    last_values_array_code = ""
    hysteresis_code_end_tag = ""
    if data_type.upper() == "WORD":
        hysteresis = Obj35mMeTe.objects.filter(DeviceName=device_name).first().Hysteresis
    if hysteresis:
        hysteresis_definition = ("aHysteresis : ARRAY[1..{}] OF INT := " + "[" + hysteresis + "];").format(num_objects)
        hyst_cdtn = "IF (aSignals[iN] > (aSignalsInternal[iN] + ((aHysteresis[iN] / 100) * aSignalsInternal[iN]))) " + \
                    "OR (aSignals[iN] < (aSignalsInternal[iN] - ((aHysteresis[iN] / 100) * aSignalsInternal[iN]))) THEN"
        last_values_array_definition = "aSignalsInternal : ARRAY[1..{}] OF {};".format(num_objects, data_type.upper())
        last_values_array_code = "aSignalsInternal[iN] := aSignals[iN];"
        hysteresis_code_end_tag = "END_IF"

    # variable definition
    declaration_info = declaration_info.format(
        pou_name,
        num_objects, data_type.upper(),
        num_objects,
        num_objects,
        num_objects,
        hysteresis_definition,
        last_values_array_definition
    )

    # ST Code block
    st_code_info = st_code_info.format(
        last_values_array_code,
        data_type.upper(),
        hyst_cdtn,
        hysteresis_code_end_tag,
        pou_name
    )

    # Write data stream
    save_.write(
        declaration_info +
        "\n" +
        st_code_info
    )

    # Closing file
    save_.close()

    return pou_name


def _sbo(device_name, data_type, num_objects, purpose, server_iteration):
    # Obtain instance information
    declaration_info = Sbo.objects.filter(Version="sbov0").first().VariableDeclaration
    body_info = Sbo.objects.filter(Version="sbov0").first().Body
    core_info = Sbo.objects.filter(Version="sbov0").first().Core
    final_check_info = Sbo.objects.filter(Version="sbov0").first().FinalCheck

    # Meta-data
    pou_name = "Sbo" + str(num_objects) + data_type + str(device_name) + purpose + str(server_iteration)

    # create file
    sbo_ = open(path + "\\" + pou_name + ".EXP", "w+")

    # Inputs
    input_str = ["xInput{}, ".format(i + 1) for i in range(num_objects)]
    input_str = ''.join(input_str)
    input_str = input_str[:-2]

    status_str = ["Status{}, ".format(i + 1) for i in range(int(num_objects / 2))]
    status_str = ''.join(status_str)
    status_str = status_str[:-2]

    # Outputs
    select_str = ["xSelect{}, ".format(i + 1) for i in range(int(num_objects / 2))]
    select_str = ''.join(select_str)
    select_str = select_str[:-2]

    execute_str = ["xExecute{}, ".format(i + 1) for i in range(int(num_objects / 2))]
    execute_str = ''.join(execute_str)
    execute_str = execute_str[:-2]

    # Internal variables
    internal_str = ["xFlag{}, ".format(i + 1) for i in range(int(num_objects / 2))]
    internal_str = ''.join(internal_str)
    internal_str = internal_str[:-2]

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
            (s * 2) + 1, (s * 2) + 2,
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
    final_str = ["xFlag{} OR ".format(i + 1) for i in range(int(num_objects / 2))]
    final_str = ''.join(final_str)
    final_str = final_str[:-4]

    final_check_info = final_check_info.format(
        final_str
    )

    # Assemble body content
    core_info_formatted += final_check_info
    body_info = body_info.format(core_info_formatted)

    # Write data stream
    sbo_.write(
        declaration_info +
        "\n" +
        body_info
    )

    sbo_.close()

    return pou_name


def _rtu(device_name, device_operation, data_type, num_objects, purpose, instance_list, server_iteration):
    # Obtain instance information
    declaration_info = Rtu.objects.filter(Version="rtuv0").first().VariableDeclaration
    sbo_variables_info = Rtu.objects.filter(Version="rtuv0").first().SboVariables
    fbd_header_info = FbdTemplate.objects.first().Header

    # Meta-data
    pou_name = "Rtu" + str(num_objects) + data_type + str(device_name) + purpose + str(server_iteration)

    # create file
    rtu_ = open(path + "\\" + pou_name + ".EXP", "w+")

    # variable definition
    # Inputs
    input_str = [input_dictionary[data_type.upper()] + "Input{}, ".format(i + 1) for i in range(num_objects)]
    input_str = ''.join(input_str)
    input_str = input_str[:-2]
    input_str += ": " + data_type.upper() + ";" + "\n"

    save_str = ["xSave{}, ".format(i + 1) for i in range(num_objects)]
    save_str = ''.join(save_str)
    save_str = save_str[:-2]

    name_str = ["sName{}, ".format(i + 1) for i in range(num_objects)]
    name_str = ''.join(name_str)
    name_str = name_str[:-2]

    trigger_str = ""
    if purpose == 'c':
        trigger_str = ["xTrigger{}, ".format(i + 1) for i in range(num_objects)]
        trigger_str = ''.join(trigger_str)
        trigger_str = trigger_str[:-2]
        trigger_str += ": BOOL;" + "\n"

    status_str = ""
    if device_operation == "SBO" and purpose == 'c':
        status_str = ["Status{}, ".format(i + 1) for i in range(int(num_objects / 2))]
        status_str = ''.join(status_str)
        status_str = status_str[:-2]
        status_str += ": ENUM870_CLIENT_COMMAND;" + "\n"

    # Outputs
    output_str = [input_dictionary[data_type.upper()] + "Output{}, ".format(i + 1) for i in range(num_objects)]
    output_str = ''.join(output_str)
    output_str = output_str[:-2]
    output_str += ": " + data_type.upper() + ";" + "\n"

    select_str = ""
    execute_str = ""
    if device_operation == "SBO" and purpose == 'c':
        select_str = ["xSelect{}, ".format(i + 1) for i in range(int(num_objects / 2))]
        select_str = ''.join(select_str)
        select_str = select_str[:-2]
        select_str += ": " + data_type.upper() + ";" + "\n"

        execute_str = ["xExecute{}, ".format(i + 1) for i in range(int(num_objects / 2))]
        execute_str = ''.join(execute_str)
        execute_str = execute_str[:-2]
        execute_str += ": " + data_type.upper() + ";" + "\n"

    # Internal variables
    instance_block = ""
    for item in instance_list:
        if 'Save' not in item[1]:
            instance_block += item[0] + item[1] + " : " + item[1] + ";" + "\n"

    sbo_internal_variables = ""
    if device_operation == "SBO" and purpose == 'c':
        sbo_internal_variables = sbo_variables_info

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
        sbo_internal_variables
    )

    rtu_.write(declaration_info + "\n")

    # FBD Code
    # Select body networks
    if device_operation == "SBO" and purpose == 'c':
        body_networks = 9
    else:
        body_networks = 6
    fbd_header_info = fbd_header_info.format(str(body_networks) + "\n")
    rtu_.write(fbd_header_info)

    # Instantiation
    # la idea es que toda la información necesaria ya esté integrada en una lista de variables, de forma que el proceso
    # se automatice
    # for instance in instance_list:
    #     if 'Sbo' in instance[1] and purpose == 'c':
    #         _jump_fbd('xJumpSelectAndExecute', 'SBO', rtu_)
    #     elif ''

    if device_operation == "SBO" and purpose == 'c':
        _jump_fbd('xJumpSelectAndExecute', 'SBO', rtu_)
    _map_fbd(instance_list[0], num_objects, data_type, purpose, rtu_)
    pack_out_0 = _pack_fbd(instance_list[1], num_objects, data_type, 'Input', rtu_)
    pack_out_1 = _pack_fbd(instance_list[2], num_objects, 'bool', 'Save', rtu_)
    pack_out_2 = _pack_fbd(instance_list[3], num_objects, 'string', 'Name', rtu_)
    check_out_0 = _check_fbd(instance_list[4], pack_out_0, rtu_)
    _save_fbd(instance_list[5], num_objects, pack_out_0, pack_out_2, check_out_0[0], pack_out_1, check_out_0[1], rtu_)
    if device_operation == "SBO" and purpose == 'c':
        _sbo_fbd(instance_list[6], num_objects, 'SBO', check_out_0[0], rtu_)
        _jump_fbd('xJumpRetry', 'SBO', rtu_)

    # Final tag
    rtu_.write("END_FUNCTION_BLOCK" + "\n")
    rtu_.close()

    return pou_name


def _jump_fbd(signal, step, file):
    fbd_jump_info = FbdTemplate.objects.first().Jump
    fbd_jump_info = fbd_jump_info.format(step)

    fbd_input_unit_info = FbdTemplate.objects.first().InputUnit
    fbd_input_unit_info = fbd_input_unit_info.format(signal)

    file.write(
        fbd_jump_info +
        "\n" +
        fbd_input_unit_info +
        "\n"
    )


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

    return output_dictionary[signal.upper()]


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
    if device_operation == 'SBO' and io_sequence[0] == 'Command':
        file.write("_BOX_EXPR : " + str((io_sequence[1] * 3) + int(io_sequence[1] / 2) + 5) + "\n")
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
            file.write("_BOX_EXPR : " + str(len(device[2][i]) * 3 + len(device[3][i]) * 3 + len(device[4][i]) * 3 +
                                            int(len(device[4][i]) / 2) + 5) + "\n")
        else:
            file.write("_BOX_EXPR : " + str(len(device[2][i]) * 3 + len(device[3][i]) * 3 + len(device[4][i]) * 3 + 5) +
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
