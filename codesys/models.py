from django.db import models
import copy
from support_functions import variable_to_declaration
from server_parts.models import Obj35mMeTe
import pou
import re

# Pou versions menu
user_prg_version = 'userprgv0'
device_version = 'devicev0'
rtu_version = 'rtuv0'
pack_version = 'packv0'
check_version = 'checkv0'
map_version = 'mapv0'
rise_version = 'risev0'
save_version = 'savev0'
sbo_version = 'sbov0'
handler_version = 'handlerv0'


# Create your models here.
class FBDTemplate(models.Model):
    DeclarationAttributes = models.TextField(default="")
    DeclarationFBHeader = models.CharField(max_length=255, default="")
    DeclarationFHeader = models.CharField(max_length=255, default="")
    DeclarationInput = models.TextField(default="")
    DeclarationOutput = models.TextField(default="")
    DeclarationInternal = models.TextField(default="")
    DeclarationEndTag = models.CharField(max_length=255, default="")
    Header = models.TextField(default="")
    FunctionBlockInputHeader = models.TextField(default="")
    FunctionInputHeader = models.TextField(default="")
    InputUnit = models.TextField(default="")
    FunctionBlockOutputHeader = models.TextField(default="")
    FunctionOutputHeader = models.TextField(default="")
    OutputUnit = models.TextField(default="")
    CodeEndTag = models.CharField(max_length=255, default="")

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(FBDTemplate, self).save()
        pou.fbd_model = FunctionBlockDiagramModel()


class UserPrg(models.Model):
    Version = models.CharField(max_length=255, default="")
    FirstCycle = models.CharField(max_length=255, default="")
    FirstCycleDataType = models.CharField(max_length=255, default="")
    MaskLocRem = models.CharField(max_length=255, default="")
    MaskLocRemDataType = models.CharField(max_length=255, default="")
    LocRemState = models.CharField(max_length=255, default="")
    LocRemStateDataType = models.CharField(max_length=255, default="")

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(UserPrg, self).save()
        pou.user_prg_model = UserPrgModel(pou.fbd_model, user_prg_version)

    def __str__(self):
        return self.Version


class Device(models.Model):
    Version = models.CharField(max_length=255, default="")
    SequenceOrder = models.CharField(max_length=255, default="")
    SequenceOrderDataType = models.CharField(max_length=255, default="")
    Protocol = models.CharField(max_length=255, default="")
    ProtocolDataType = models.CharField(max_length=255, default="")
    StateLocRem = models.CharField(max_length=255, default="")
    StateLocRemDataType = models.CharField(max_length=255, default="")
    Measure = models.CharField(max_length=255, default="")
    MeasureDataType = models.CharField(max_length=255, default="")
    MeasureOutput = models.CharField(max_length=255, default="")
    MeasureOutputDataType = models.CharField(max_length=255, default="")
    SaveMeasure = models.CharField(max_length=255, default="")
    SaveMeasureDataType = models.CharField(max_length=255, default="")
    NameMeasure = models.CharField(max_length=255, default="")
    NameMeasureDataType = models.CharField(max_length=255, default="")
    State = models.CharField(max_length=255, default="")
    StateDataType = models.CharField(max_length=255, default="")
    StateOutput = models.CharField(max_length=255, default="")
    StateOutputDataType = models.CharField(max_length=255, default="")
    SaveState = models.CharField(max_length=255, default="")
    SaveStateDataType = models.CharField(max_length=255, default="")
    NameState = models.CharField(max_length=255, default="")
    NameStateDataType = models.CharField(max_length=255, default="")
    RiseState = models.CharField(max_length=255, default="")
    RiseStateDataType = models.CharField(max_length=255, default="")
    Command = models.CharField(max_length=255, default="")
    CommandDataType = models.CharField(max_length=255, default="")
    CommandOutput = models.CharField(max_length=255, default="")
    CommandOutputDataType = models.CharField(max_length=255, default="")
    SaveCommand = models.CharField(max_length=255, default="")
    SaveCommandDataType = models.CharField(max_length=255, default="")
    NameCommand = models.CharField(max_length=255, default="")
    NameCommandDataType = models.CharField(max_length=255, default="")
    TriggerCommand = models.CharField(max_length=255, default="")
    TriggerCommandDataType = models.CharField(max_length=255, default="")
    Status = models.CharField(max_length=255, default="")
    StatusDataType = models.CharField(max_length=255, default="")
    Select = models.CharField(max_length=255, default="")
    SelectDataType = models.CharField(max_length=255, default="")
    Execute = models.CharField(max_length=255, default="")
    ExecuteDataType = models.CharField(max_length=255, default="")

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(Device, self).save()
        pou.device_model = DeviceModel(pou.user_prg_model, device_version)

    def __str__(self):
        return self.Version


class Rtu(models.Model):
    Version = models.CharField(max_length=255, default="")
    Action = models.CharField(max_length=255, default="")
    ActionDataType = models.CharField(max_length=255, default="")
    RiseChanges = models.CharField(max_length=255, default="")
    RiseChangesDataType = models.CharField(max_length=255, default="")
    TriggerChanges = models.CharField(max_length=255, default="")
    TriggerChangesDataType = models.CharField(max_length=255, default="")
    Signals = models.CharField(max_length=255, default="")
    SignalsDataType = models.CharField(max_length=255, default="")
    CheckChanges = models.CharField(max_length=255, default="")
    CheckChangesDataType = models.CharField(max_length=255, default="")
    Names = models.CharField(max_length=255, default="")
    NamesDataType = models.CharField(max_length=255, default="")
    Saves = models.CharField(max_length=255, default="")
    SavesDataType = models.CharField(max_length=255, default="")
    Error = models.CharField(max_length=255, default="")
    ErrorDataType = models.CharField(max_length=255, default="")

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(Rtu, self).save()
        pou.rtu_model = RtuModel(pou.device_model, rtu_version)

    def __str__(self):
        return self.Version


class Pack(models.Model):
    Version = models.CharField(max_length=255)
    ST = models.TextField(default="")

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(Pack, self).save()
        pou.pack_model = PackModel(pou.rtu_model, pack_version)

    def __str__(self):
        return self.Version


class Check(models.Model):
    Version = models.CharField(max_length=255)
    Iterator = models.CharField(max_length=255, default="")
    IteratorDataType = models.CharField(max_length=255, default="")
    LastValues = models.CharField(max_length=255, default="")
    LastValuesDataType = models.CharField(max_length=255, default="")
    ST = models.TextField()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(Check, self).save()
        pou.check_model = CheckModel(pou.rtu_model, check_version)

    def __str__(self):
        return self.Version


class Map(models.Model):
    Version = models.CharField(max_length=255)
    ST = models.TextField(default="")

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(Map, self).save()
        pou.pack_model = PackModel(pou.rtu_model, map_version)

    def __str__(self):
        return self.Version


class RiseToTrigger(models.Model):
    Version = models.CharField(max_length=255)
    LastRise = models.CharField(max_length=255, default="")
    LastRiseDataType = models.CharField(max_length=255, default="")
    Iterator = models.CharField(max_length=255, default="")
    IteratorDataType = models.CharField(max_length=255, default="")
    ST = models.TextField(default="")

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(RiseToTrigger, self).save()
        pou.rise_model = RiseModel(pou.rtu_model, rise_version)

    def __str__(self):
        return self.Version


class Save(models.Model):
    Version = models.CharField(max_length=255)
    Reason = models.CharField(max_length=255, default="")
    ReasonDataType = models.CharField(max_length=255, default="")
    ReasonInitVal = models.CharField(max_length=255, default="")
    Time = models.CharField(max_length=255, default="")
    TimeDataType = models.CharField(max_length=255, default="")
    Offset = models.CharField(max_length=255, default="")
    OffsetDataType = models.CharField(max_length=255, default="")
    Iterator = models.CharField(max_length=255, default="")
    IteratorDataType = models.CharField(max_length=255, default="")
    PowerOnPrefix = models.CharField(max_length=255, default="")
    PowerOnPrefixDataType = models.CharField(max_length=255, default="")
    PowerOnPrefixInitVal = models.CharField(max_length=255, default="")
    PrefixUnderLine = models.CharField(max_length=255, default="")
    PrefixUnderLineDataType = models.CharField(max_length=255, default="")
    PrefixUnderLineInitVal = models.CharField(max_length=255, default="")
    Delimiter = models.CharField(max_length=255, default="")
    DelimiterDataType = models.CharField(max_length=255, default="")
    DelimiterInitVal = models.CharField(max_length=255, default="")
    ObjectValue = models.CharField(max_length=255, default="")
    ObjectValueDataType = models.CharField(max_length=255, default="")
    Prefix = models.CharField(max_length=255, default="")
    PrefixDataType = models.CharField(max_length=255, default="")
    File = models.CharField(max_length=255, default="")
    FileDataType = models.CharField(max_length=255, default="")
    Close = models.CharField(max_length=255, default="")
    CloseDataType = models.CharField(max_length=255, default="")
    NewLine = models.CharField(max_length=255, default="")
    NewLineDataType = models.CharField(max_length=255, default="")
    NewLineInitVal = models.CharField(max_length=255, default="")
    Hysteresis = models.CharField(max_length=255, default="")
    HysteresisDataType = models.CharField(max_length=255, default="")
    LastValues = models.CharField(max_length=255, default="")
    LastValuesDataType = models.CharField(max_length=255, default="")
    ST = models.TextField(default="")

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(Save, self).save()
        pou.save_model = SaveModel(pou.rtu_model, save_version)

    def __str__(self):
        return self.Version


class Sbo(models.Model):
    Version = models.CharField(max_length=255)
    ErrorStatInternal = models.CharField(max_length=255, default="")
    ErrorStatInternalDataType = models.CharField(max_length=255, default="")
    Flag = models.CharField(max_length=255, default="")
    FlagDataType = models.CharField(max_length=255, default="")
    STBody = models.TextField(default="")
    STCore = models.TextField(default="")

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(Sbo, self).save()
        pou.sbo_model = SboModel(pou.rtu_model, sbo_version)

    def __str__(self):
        return self.Version


class Handler(models.Model):
    Version = models.CharField(max_length=255)
    ErrorDescription = models.CharField(max_length=255, default="")
    ErrorDescriptionDataType = models.CharField(max_length=255, default="")
    ST = models.TextField(default="")

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(Handler, self).save()
        pou.handler_model = HandlerModel(pou.rtu_model, handler_version)

    def __str__(self):
        return self.Version


class FunctionBlockDiagramModel:
    def __init__(self):
        self.function_block_diagram_template = FBDTemplate.objects.first()
        self.declaration_attributes = self.function_block_diagram_template.DeclarationAttributes
        self.declaration_fb_header = re.sub(r'(?<={).+?(?=})', '', self.function_block_diagram_template.DeclarationFBHeader)
        self.declaration_f_header = re.sub(r'(?<={).+?(?=})', '', self.function_block_diagram_template.DeclarationFHeader)
        self.declaration_input = re.sub(r'(?<={).+?(?=})', '', self.function_block_diagram_template.DeclarationInput)
        self.declaration_output = re.sub(r'(?<={).+?(?=})', '', self.function_block_diagram_template.DeclarationOutput)
        self.declaration_internal = re.sub(r'(?<={).+?(?=})', '', self.function_block_diagram_template.DeclarationInternal)
        self.declaration_end_tag = self.function_block_diagram_template.DeclarationEndTag
        self.header = re.sub(r'(?<={).+?(?=})', '', self.function_block_diagram_template.Header)
        self.function_block_input_header = re.sub(r'(?<={).+?(?=})', '', self.function_block_diagram_template.FunctionBlockInputHeader)
        self.function_input_header = re.sub(r'(?<={).+?(?=})', '', self.function_block_diagram_template.FunctionInputHeader)
        self.input_unit = re.sub(r'(?<={).+?(?=})', '', self.function_block_diagram_template.InputUnit)
        self.function_block_output_header = re.sub(r'(?<={).+?(?=})', '', self.function_block_diagram_template.FunctionBlockOutputHeader)
        self.function_output_header = re.sub(r'(?<={).+?(?=})', '', self.function_block_diagram_template.FunctionOutputHeader)
        self.output_unit = re.sub(r'(?<={).+?(?=})', '', self.function_block_diagram_template.OutputUnit)
        self.code_end_tag = self.function_block_diagram_template.CodeEndTag


class UserPrgModel(FunctionBlockDiagramModel):
    # Copy constructor implementation
    def __init__(self, fbd, version):
        if fbd:
            self.__dict__ = copy.deepcopy(fbd.__dict__)
        else:
            FunctionBlockDiagramModel.__init__(self)

        self.user_prg_model = UserPrg.objects.filter(Version=version).first()
        self.first_cycle = self.user_prg_model.FirstCycle
        self.first_cycle_data_type = self.user_prg_model.FirstCycleDataType
        self.mask_loc_rem = self.user_prg_model.MaskLocRem
        self.mask_loc_rem_data_type = self.user_prg_model.MaskLocRemDataType
        self.loc_rem_state = self.user_prg_model.LocRemState
        self.loc_rem_state_data_type = self.user_prg_model.LocRemStateDataType


class DeviceModel(UserPrgModel):
    # Copy constructor implementation
    def __init__(self, user_prg, version):
        if user_prg:
            self.__dict__ = copy.deepcopy(user_prg.__dict__)
        else:
            UserPrgModel.__init__(self, None, None)

        self.device_model = Device.objects.filter(Version=version).first()
        self.sequence_order = self.device_model.SequenceOrder
        self.sequence_order_data_type = self.device_model.SequenceOrderDataType
        self.protocol = self.device_model.Protocol
        self.protocol_data_type = self.device_model.ProtocolDataType
        self.state_loc_rem = self.device_model.StateLocRem
        self.state_loc_rem_data_type = self.device_model.StateLocRemDataType
        self.measure = self.device_model.Measure
        self.measure_data_type = self.device_model.MeasureDataType
        self.measure_output = self.device_model.MeasureOutput
        self.measure_output_data_type = self.device_model.MeasureOutputDataType
        self.save_measure = self.device_model.SaveMeasure
        self.save_measure_data_type = self.device_model.SaveMeasureDataType
        self.name_measure = self.device_model.NameMeasure
        self.name_measure_data_type = self.device_model.NameMeasureDataType
        self.state = self.device_model.State
        self.state_data_type = self.device_model.StateDataType
        self.state_output = self.device_model.StateOutput
        self.state_output_data_type = self.device_model.StateOutputDataType
        self.save_state = self.device_model.SaveState
        self.save_state_data_type = self.device_model.SaveStateDataType
        self.name_state = self.device_model.NameState
        self.name_state_data_type = self.device_model.NameStateDataType
        self.rise_state = self.device_model.RiseState
        self.rise_state_data_type = self.device_model.RiseStateDataType
        self.command = self.device_model.Command
        self.command_data_type = self.device_model.CommandDataType
        self.command_output = self.device_model.CommandOutput
        self.command_output_data_type = self.device_model.CommandOutputDataType
        self.save_command = self.device_model.SaveCommand
        self.save_command_data_type = self.device_model.SaveCommandDataType
        self.name_command = self.device_model.NameCommand
        self.name_command_data_type = self.device_model.NameCommandDataType
        self.trigger_command = self.device_model.TriggerCommand
        self.trigger_command_data_type = self.device_model.TriggerCommandDataType
        self.status = self.device_model.Status
        self.status_data_type = self.device_model.StatusDataType
        self.select = self.device_model.Select
        self.select_data_type = self.device_model.Select
        self.execute = self.device_model.Execute
        self.execute_data_type = self.device_model.ExecuteDataType

    def device(self, device_name, device_operation, rtu_instance_list, rtu, server_iteration, path):
        # Meta-data
        pou_name = "Dev" + str(device_name) + str(server_iteration)

        # create file
        device_object = open(path + "\\" + pou_name + ".EXP", "w+")

        # variable definition
        # inputs
        # control inputs
        input_str = f"{self.sequence_order} : {self.sequence_order_data_type}" + '\n'
        input_str += f"{self.protocol} : {self.protocol_data_type}" + '\n'
        input_str += f"{self.state_loc_rem} : {self.state_loc_rem_data_type}" + '\n'

        # measures
        input_str += variable_to_declaration(self.measure, rtu[0][0], self.measure_data_type) + '\n'
        input_str += variable_to_declaration(self.save_measure, rtu[0][0], self.save_measure_data_type) + '\n'
        input_str += variable_to_declaration(self.name_measure, rtu[0][0], self.name_measure_data_type) + '\n'

        # states
        input_str += variable_to_declaration(self.state, rtu[1][0], self.state_data_type) + '\n'
        input_str += variable_to_declaration(self.save_state, rtu[1][0], self.save_state_data_type) + '\n'
        input_str += variable_to_declaration(self.name_state, rtu[1][0], self.name_state_data_type) + '\n'
        input_str += variable_to_declaration(self.rise_state, rtu[1][0], self.rise_state_data_type) + '\n'

        # commands
        input_str += variable_to_declaration(self.command, rtu[2][0], self.command_data_type) + '\n'
        input_str += variable_to_declaration(self.save_command, rtu[2][0], self.save_command_data_type) + '\n'
        input_str += variable_to_declaration(self.name_command, rtu[2][0], self.name_command_data_type) + '\n'
        input_str += variable_to_declaration(self.trigger_command, rtu[2][0], self.trigger_command_data_type) + '\n'

        # inputs sbo
        if device_operation == "SBO":
            input_str += variable_to_declaration(self.status, int(rtu[2][0] / 2),  self.status_data_type) + '\n'

        # Outputs
        # measures
        output_str = variable_to_declaration(self.measure_output, rtu[0][0], self.measure_output_data_type) + '\n'

        # states
        output_str += variable_to_declaration(self.state_output, rtu[1][0], self.state_output_data_type) + '\n'

        # commands
        output_str += variable_to_declaration(self.command_output, rtu[2][0], self.command_output_data_type) + '\n'

        # outputs sbo
        if device_operation == "SBO":
            output_str += variable_to_declaration(self.select, int(rtu[2][0] / 2), self.select_data_type) + '\n'
            output_str += variable_to_declaration(self.execute, int(rtu[2][0] / 2), self.execute_data_type) + '\n'

        # Internals
        internal_str = ''
        for instance in rtu_instance_list:
            internal_str += f"inst0{instance} : {instance};" + '\n'

        # Declaration construction
        declaration = self.declaration_attributes + '\n'
        declaration += self.declaration_fb_header.format(pou_name) + '\n'
        declaration += self.declaration_input.format(input_str) + '\n'
        declaration += self.declaration_output.format(output_str) + '\n'
        declaration += self.declaration_internal.format(internal_str) + '\n'
        declaration += self.declaration_end_tag + '\n'
        device_object.write(declaration)

        # Code construction
        device_object.write(self.header.format(str(len(rtu))) + '\n')

        # Instantiation
        for i in range(len(rtu)):
            self._rtu_fbd(device_operation, rtu_instance_list[i], rtu[i], device_object)

        # Final tag
        device_object.write(self.code_end_tag + '\n')

        # Closing file
        device_object.close()

        return pou_name

    def _rtu_fbd(self, device_operation, instance, sequence, file):
        # Obtaining data
        num_objects = sequence[0]
        purpose = sequence[1]

        rtu_information = self.rtu_decision_tree(purpose)
        input_data = rtu_information['input_data']
        output_data = rtu_information['output_data']
        save_data = rtu_information['save_data']
        name_data = rtu_information['name_data']
        trigger_data = rtu_information['trigger_data']

        # Number of inputs
        num_inputs = 0
        if purpose == 'measure':
            num_inputs = (3 * num_objects) + 5
        elif purpose == 'state':
            num_inputs = (4 * num_objects) + 5
        elif purpose == 'command':
            if device_operation == 'SBO':
                num_inputs = (4 * num_objects) + (num_objects / 2) + 5
            else:
                num_inputs = (4 * num_objects) + 5

        # Input header
        fbd_str = self.function_block_input_header.format(f"inst0{instance}", f"{num_inputs}") + '\n'

        # Inputs
        # header
        fbd_str += self.input_unit.format(f"{self.first_cycle}") + '\n'
        fbd_str += self.input_unit.format(f"{self.sequence_order}") + '\n'
        fbd_str += self.input_unit.format(f"{self.protocol}") + '\n'
        fbd_str += self.input_unit.format(f"{self.state_loc_rem}") + '\n'
        if purpose == 'command':
            fbd_str += self.input_unit.format("CONTROL") + '\n'
        else:
            fbd_str += self.input_unit.format("MONITOR") + '\n'

        # input data
        for i in range(num_objects):
            fbd_str += self.input_unit.format(f"{input_data}{i + 1}") + '\n'

        # saves
        for i in range(num_objects):
            fbd_str += self.input_unit.format(f"{save_data}{i + 1}") + '\n'

        # names
        for i in range(num_objects):
            fbd_str += self.input_unit.format(f"{name_data}{i + 1}") + '\n'

        # trigger and status
        if purpose != 'measure':
            for i in range(num_objects):
                fbd_str += self.input_unit.format(f"{trigger_data}{i + 1}") + '\n'
            if purpose == 'command' and device_operation == 'SBO':
                for i in range(int(num_objects / 2)):
                    fbd_str += self.input_unit.format(f"{self.status}{i + 1}") + '\n'

        # Number of outputs
        num_outputs = 0
        if purpose == 'command' and device_operation == 'SBO':
            num_outputs = (2 * num_objects) - 1
        else:
            num_outputs = num_objects - 1

        # output header 1
        fbd_str += self.function_block_output_header.format(f"{instance}", f"{num_outputs}") + '\n'

        # output unit 1
        for i in range(num_objects - 1):
            fbd_str += self.output_unit.format(f"{output_data}{i + 2}") + '\n'

        if purpose == 'command' and device_operation == 'SBO':
            for i in range(int(num_objects / 2)):
                fbd_str += self.output_unit.format(f"{self.select}{i + 1}") + '\n'
            for i in range(int(num_objects / 2)):
                fbd_str += self.output_unit.format(f"{self.execute}{i + 1}") + '\n'

        # Output header 2
        fbd_str += self.function_block_output_header.format("", "1") + '\n'

        # output unit 2
        fbd_str += self.output_unit.format(f"{output_data}1") + '\n'

        # Writing the fbd
        file.write(fbd_str)

    def rtu_decision_tree(self, purpose):
        response = {
            'input_data': '',
            'input_data_type': '',
            'output_data': '',
            'output_data_type': '',
            'save_data': '',
            'save_data_type': '',
            'name_data': '',
            'name_data_type': '',
            'trigger_data': '',
            'trigger_data_type': ''
        }
        if purpose == 'command':
            response['input_data'] = self.command
            response['input_data_type'] = self.command_data_type
            response['output_data'] = self.command_output
            response['output_data_type'] = self.command_output_data_type
            response['save_data'] = self.save_command
            response['save_data_type'] = self.save_command_data_type
            response['name_data'] = self.name_command
            response['name_data_type'] = self.name_command_data_type
            response['trigger_data'] = self.trigger_command
            response['trigger_data_type'] = self.trigger_command_data_type
        elif purpose == 'state':
            response['input_data'] = self.state
            response['input_data_type'] = self.state_data_type
            response['output_data'] = self.state_output
            response['output_data_type'] = self.state_output_data_type
            response['save_data'] = self.save_state
            response['save_data_type'] = self.save_state_data_type
            response['name_data'] = self.name_state
            response['name_data_type'] = self.name_state_data_type
            response['trigger_data'] = self.rise_state
            response['trigger_data_type'] = self.rise_state_data_type
        elif purpose == 'measure':
            response['input_data'] = self.measure
            response['input_data_type'] = self.measure_data_type
            response['output_data'] = self.measure_output
            response['output_data_type'] = self.measure_output_data_type
            response['save_data'] = self.save_measure
            response['save_data_type'] = self.save_measure_data_type
            response['name_data'] = self.name_measure
            response['name_data_type'] = self.name_measure_data_type

        return response


class RtuModel(DeviceModel):
    # Copy constructor implementation
    def __init__(self, device, version):
        if device:
            self.__dict__ = copy.deepcopy(device.__dict__)
        else:
            DeviceModel.__init__(self, None, None)

        self.rtu_model = Rtu.objects.filter(Version=version).first()
        self.action = self.rtu_model.Action
        self.action_data_type = self.rtu_model.ActionDataType
        self.rise_changes = self.rtu_model.RiseChanges
        self.rise_changes_data_type = self.rtu_model.RiseChangesDataType
        self.trigger_changes = self.rtu_model.TriggerChanges
        self.trigger_changes_data_type = self.rtu_model.TriggerChangesDataType
        self.signals = self.rtu_model.Signals
        self.signals_data_type = self.rtu_model.SignalsDataType
        self.check_changes = self.rtu_model.CheckChanges
        self.check_changes_data_type = self.rtu_model.CheckChangesDataType
        self.names = self.rtu_model.Names
        self.names_data_type = self.rtu_model.NamesDataType
        self.saves = self.rtu_model.Saves
        self.saves_data_type = self.rtu_model.SavesDataType
        self.error = self.rtu_model.Error
        self.error_data_type = self.rtu_model.ErrorDataType

    def rtu(self, device_name, device_operation, num_objects, purpose, instance_list, server_iteration, path):
        # Obtaining data
        rtu_information = self.rtu_decision_tree(purpose)
        input_data = rtu_information['input_data']
        input_data_type = rtu_information['input_data_type']
        output_data = rtu_information['output_data']
        output_data_type = rtu_information['output_data_type']
        save_data = rtu_information['save_data']
        save_data_type = rtu_information['save_data_type']
        name_data = rtu_information['name_data']
        name_data_type = rtu_information['name_data_type']
        trigger_data = rtu_information['trigger_data']
        trigger_data_type = rtu_information['trigger_data_type']

        # Instance data
        pou_name = "Rtu" + str(num_objects) + str(device_name) + purpose + str(server_iteration)

        # create file
        rtu_object = open(path + "\\" + pou_name + ".EXP", "w+")

        # variable definition
        # Inputs
        input_str = f"{self.first_cycle} : {self.first_cycle_data_type};" + '\n'
        input_str += f"{self.sequence_order} : {self.sequence_order};" + '\n'
        input_str += f"{self.protocol} : {self.protocol_data_type};" + '\n'
        input_str += f"{self.state_loc_rem} : {self.state_loc_rem_data_type};" + '\n'
        input_str += f"{self.action} : {self.action_data_type};" + '\n'
        input_str += variable_to_declaration(signal=input_data, num_objects=num_objects, data_type=input_data_type) + '\n'
        input_str += variable_to_declaration(signal=save_data, num_objects=num_objects, data_type=save_data_type) + '\n'
        input_str += variable_to_declaration(signal=name_data, num_objects=num_objects, data_type=name_data_type) + '\n'

        if purpose != 'measure':
            input_str += variable_to_declaration(signal=trigger_data, num_objects=num_objects, data_type=trigger_data_type) + '\n'

        if device_operation == "SBO" and purpose == 'command':
            input_str += variable_to_declaration(signal=self.status, num_objects=int(num_objects / 2), data_type=self.status_data_type) + '\n'

        # Outputs
        output_str = variable_to_declaration(signal=output_data, num_objects=num_objects, data_type=output_data_type) + '\n'

        if device_operation == "SBO" and purpose == 'command':
            output_str += variable_to_declaration(signal=self.select, num_objects=num_objects, data_type=self.select) + '\n'
            output_str += variable_to_declaration(signal=self.execute, num_objects=num_objects, data_type=self.execute) + '\n'

        # Internals
        internal_str = f"{self.action} : {self.action_data_type};" + '\n'
        internal_str += f"{self.signals} : ARRAY [1..{num_objects}] OF {input_data_type};" + '\n'
        internal_str += f"{self.check_changes} : ARRAY [1..{num_objects}] OF {self.check_changes_data_type};" + '\n'
        internal_str += f"{self.names} : ARRAY [1..{num_objects}] OF {self.names_data_type}" + '\n'
        internal_str += f"{self.saves} : ARRAY [1..{num_objects}] OF {self.saves_data_type}" + '\n'
        internal_str += f"{self.error} : ARRAY [1..{num_objects}] OF {self.error_data_type}" + '\n'

        if purpose != 'measure':
            internal_str += f"{self.trigger_changes} : ARRAY [1..{num_objects}] OF {self.trigger_changes_data_type}" + '\n'
            if purpose == 'state':
                internal_str += f"{self.rise_changes} : ARRAY [1..{num_objects}] OF {self.rise_changes_data_type}" + '\n'

        for item in instance_list:
            if 'Save' not in item:
                internal_str += f"inst0{item} : {item};" + '\n'

        # Declaration construction
        declaration = self.declaration_attributes + '\n'
        declaration += self.declaration_fb_header.format(pou_name) + '\n'
        declaration += self.declaration_input.format(input_str) + '\n'
        declaration += self.declaration_output.format(output_str) + '\n'
        declaration += self.declaration_internal.format(internal_str) + '\n'
        declaration += self.declaration_end_tag + '\n'
        rtu_object.write(declaration)

        # FBD Code
        # Select body networks
        if purpose == 'measure':
            body_networks = 6
        else:
            if purpose == 'command':
                if device_operation == 'SBO':
                    body_networks = 9
                else:
                    body_networks = 7
            else:
                body_networks = 8

        # Writing body networks
        networks = self.header.format(body_networks)
        rtu_object.write(networks + '\n')

        # RTU hub
        if purpose == 'command':
            self._pack_fbd(instance_list[0], num_objects, purpose, 'trigger', rtu_object)
            self._pack_fbd(instance_list[1], num_objects, purpose, 'values', rtu_object)
            self._check_fbd(instance_list[2], rtu_object)
            self._map_fbd(instance_list[3], num_objects, purpose, rtu_object)
            self._pack_fbd(instance_list[4], num_objects, purpose, 'save', rtu_object)
            self._pack_fbd(instance_list[5], num_objects, purpose, 'label', rtu_object)
            self._save_fbd(instance_list[6], rtu_object)
            if device_operation == 'SBO':
                self._sbo_fbd(instance_list[7], num_objects, rtu_object)
                self._handler_fbd(instance_list[8], rtu_object)
        elif purpose == 'state':
            self._pack_fbd(instance_list[0], num_objects, purpose, 'trigger', rtu_object)
            self._rise_fbd(instance_list[1], rtu_object)
            self._pack_fbd(instance_list[2], num_objects, purpose, 'values', rtu_object)
            self._check_fbd(instance_list[3], rtu_object)
            self._map_fbd(instance_list[4], num_objects, purpose, rtu_object)
            self._pack_fbd(instance_list[5], num_objects, purpose, 'save', rtu_object)
            self._pack_fbd(instance_list[6], num_objects, purpose, 'label', rtu_object)
            self._save_fbd(instance_list[7], rtu_object)
        elif purpose == 'measure':
            self._pack_fbd(instance_list[0], num_objects, purpose, 'values', rtu_object)
            self._check_fbd(instance_list[1], rtu_object)
            self._map_fbd(instance_list[2], num_objects, purpose, rtu_object)
            self._pack_fbd(instance_list[3], num_objects, purpose, 'save', rtu_object)
            self._pack_fbd(instance_list[4], num_objects, purpose, 'label', rtu_object)
            self._save_fbd(instance_list[5], rtu_object)

        # Final tag
        rtu_object.write(self.code_end_tag + '\n')
        rtu_object.close()

        return pou_name

    def _pack_fbd(self, instance, num_objects, purpose, internal_purpose, file):
        # Obtaining data
        pack_information = self.pack_decision_tree(purpose, internal_purpose)
        input_data = pack_information[0]
        output_data = pack_information[2]

        # Input header
        fbd_str = self.function_block_input_header.format(f"inst0{instance}", str(num_objects)) + '\n'

        # Input unit
        for i in range(num_objects):
            fbd_str += self.input_unit.format(f"{input_data}{i + 1}") + '\n'

        # Output header 1
        fbd_str += self.function_block_output_header.format(f"{instance}", "0") + '\n'

        # Output header 2
        fbd_str += self.function_block_output_header.format("", "1") + '\n'

        # Output unit
        fbd_str += self.output_unit.format(output_data) + '\n'

        # Writing the fbd
        file.write(fbd_str)

    def _rise_fbd(self, instance, file):
        # Input header
        fbd_str = self.function_block_input_header.format(f"inst0{instance}", "1") + '\n'

        # Input unit
        fbd_str += self.input_unit.format(f"{self.rise_changes}") + '\n'

        # Output header 1
        fbd_str += self.function_block_output_header.format(f"{instance}", "0") + '\n'

        # Output header 2
        fbd_str += self.function_block_output_header.format("", "1") + '\n'

        # Output unit
        fbd_str += self.output_unit.format(self.trigger_changes) + '\n'

        # Writing the fbd
        file.write(fbd_str)

    def _check_fbd(self, instance, file):
        # Input header
        fbd_str = self.function_block_input_header.format(f"inst0{instance}", "2") + '\n'

        # Input unit
        fbd_str += self.input_unit.format(f"{self.signals}") + '\n'
        fbd_str += self.input_unit.format(f"{self.first_cycle}") + '\n'

        # Output header 1
        fbd_str += self.function_block_output_header.format(f"{instance}", "0") + '\n'

        # Output header 2
        fbd_str += self.function_block_output_header.format("", "1") + '\n'

        # Output unit
        fbd_str += self.output_unit.format(self.check_changes) + '\n'

        # Writing the fbd
        file.write(fbd_str)

    def _map_fbd(self, instance, num_objects, purpose, file):
        # Obtaining data
        map_information = self.map_decision_tree(purpose)
        input_data = map_information[0]
        output_data = map_information[2]

        if purpose == 'measure':
            inputs = num_objects + 2
        else:
            inputs = (3 * num_objects) + 2

        # Input header
        fbd_str = self.function_block_input_header.format(f"inst0{instance}", f"{inputs}") + '\n'

        # Input unit
        fbd_str += self.input_unit.format(f"{self.action}") + '\n'
        fbd_str += self.input_unit.format(f"{self.loc_rem_state}") + '\n'

        # inputs
        for i in range(num_objects):
            fbd_str += self.input_unit.format(f"{input_data}{i + 1}") + '\n'

        if purpose != 'measure':
            # triggers
            for i in range(num_objects):
                fbd_str += self.input_unit.format(f"{self.trigger_changes}[{i + 1}]") + '\n'

            # checks
            for i in range(num_objects):
                fbd_str += self.input_unit.format(f"{self.check_changes}[{i + 1}]") + '\n'

        # Output header 1
        fbd_str += self.function_block_output_header.format(f"{instance}", f"{num_objects - 1}") + '\n'

        # Output unit 1
        for i in range(num_objects - 1):
            fbd_str += self.output_unit.format(f"{output_data}{i + 2}") + '\n'

        # Output header 2
        fbd_str += self.function_block_output_header.format("", "1") + '\n'

        # Output unit 2
        fbd_str += self.output_unit.format(f"{output_data}1") + '\n'

        # Writing fbd
        file.write(fbd_str)

    def _save_fbd(self, instance, file):
        # Input header
        fbd_str = self.function_input_header.format("9") + '\n'

        # Input unit
        fbd_str += self.input_unit.format(f"{self.first_cycle}") + '\n'
        fbd_str += self.input_unit.format(f"{self.sequence_order}") + '\n'
        fbd_str += self.input_unit.format(f"{self.protocol}") + '\n'
        fbd_str += self.input_unit.format(f"{self.signals}") + '\n'
        fbd_str += self.input_unit.format(f"{self.names}") + '\n'
        fbd_str += self.input_unit.format(f"{self.trigger_changes}") + '\n'
        fbd_str += self.input_unit.format(f"{self.state_loc_rem}") + '\n'
        fbd_str += self.input_unit.format(f"{self.action}") + '\n'
        fbd_str += self.input_unit.format(f"{self.saves}") + '\n'

        # Output header
        fbd_str += self.function_output_header.format(f"{instance}") + '\n'

        # Writing the fbd
        file.write(fbd_str)

    def _sbo_fbd(self, instance, num_objects, file):
        # Input header
        fbd_str = self.function_block_input_header.format(f"inst0{instance}", f"{num_objects + int(num_objects / 2) + 1}") + '\n'

        # Input unit
        fbd_str += self.input_unit.format(f"{self.state_loc_rem}") + '\n'

        # Triggers
        for i in range(num_objects):
            fbd_str += self.input_unit.format(f"{self.trigger_changes}[{i + 1}]") + '\n'

        # Status
        for i in range(int(num_objects / 2)):
            fbd_str += self.input_unit.format(f"{self.status}{i + 1}") + '\n'

        # Output header 1
        fbd_str += self.function_block_output_header.format(f"{instance}", f"{(num_objects + 1) - 1}") + '\n'

        # Selects
        for i in range(int(num_objects / 2)):
            fbd_str += self.output_unit.format(f"{self.select}{i + 1}") + '\n'

        # Executes
        for i in range(int(num_objects / 2)):
            fbd_str += self.output_unit.format(f"{self.execute}{i + 1}") + '\n'

        # Output header 2
        fbd_str += self.function_block_output_header.format("", "1") + '\n'

        # Output unit
        fbd_str += self.output_unit.format(f"{self.error}") + '\n'

        # Writing the fbd
        file.write(fbd_str)

    def _handler_fbd(self, instance, file):
        # Input header
        fbd_str = self.function_input_header.format(f"inst0{instance}", "1") + '\n'

        # Input unit
        fbd_str += self.input_unit.format(f"{self.error}") + '\n'

        # Function output header
        fbd_str += self.function_output_header.format(f"{instance}") + '\n'

        # Writing the fbd
        file.write(fbd_str)

    def pack_decision_tree(self, rtu_purpose, internal_purpose):
        input_data = ''
        output_data = ''
        input_data_type = ''
        output_data_type = ''
        if internal_purpose == 'trigger':
            if rtu_purpose == 'command':
                input_data = self.trigger_command
                output_data = self.trigger_changes
                input_data_type = self.trigger_command_data_type
                output_data_type = self.trigger_changes_data_type
            elif rtu_purpose == 'state':
                input_data = self.rise_state
                output_data = self.rise_changes
                input_data_type = self.rise_state_data_type
                output_data_type = self.rise_changes_data_type
        elif internal_purpose == 'label':
            if rtu_purpose == 'command':
                input_data = self.name_command
                input_data_type = self.name_command_data_type
            elif rtu_purpose == 'state':
                input_data = self.name_state
                input_data_type = self.name_state_data_type
            elif rtu_purpose == 'measure':
                input_data = self.name_measure
                input_data_type = self.name_measure_data_type
            output_data = self.names
            output_data_type = self.names_data_type
        elif internal_purpose == 'save':
            if rtu_purpose == 'command':
                input_data = self.save_command
                input_data_type = self.save_command_data_type
            elif rtu_purpose == 'state':
                input_data = self.save_state
                input_data_type = self.save_state_data_type
            elif rtu_purpose == 'measure':
                input_data = self.save_measure
                input_data_type = self.save_measure_data_type
            output_data = self.saves
            output_data_type = self.saves_data_type
        elif internal_purpose == 'values':
            if rtu_purpose == 'command':
                input_data = self.command
                input_data_type = self.command_data_type
                output_data_type = self.command_data_type
            elif rtu_purpose == 'state':
                input_data = self.state
                input_data_type = self.state_data_type
                output_data_type = self.state_data_type
            elif rtu_purpose == 'measure':
                input_data = self.measure
                input_data_type = self.measure_data_type
                output_data_type = self.measure_data_type
            output_data = self.signals
        else:
            "gestionar errores"

        return input_data, input_data_type, output_data, output_data_type

    def check_decision_tree(self, purpose):
        response = {
            'input_data_type': ''
        }
        if purpose == 'command':
            response['input_data_type'] = self.command_data_type
        elif purpose == 'state':
            response['input_data_type'] = self.state_data_type
        elif purpose == 'measure':
            response['input_data_type'] = self.measure_data_type

        return response

    def map_decision_tree(self, purpose):
        input_data = ''
        input_data_type = ''
        output_data = ''
        output_data_type = ''
        if purpose == 'command':
            input_data = self.command
            input_data_type = self.command_data_type
            output_data = self.command_output
            output_data_type = self.command_output_data_type
        elif purpose == 'state':
            input_data = self.state
            input_data_type = self.state_data_type
            output_data = self.state_output
            output_data_type = self.state_output_data_type
        elif purpose == 'measure':
            input_data = self.measure
            input_data_type = self.measure_data_type
            output_data = self.measure_output
            output_data_type = self.measure_output_data_type

        return input_data, input_data_type, output_data, output_data_type

    def save_decision_tree(self, purpose):
        response = {
            'input_data_type': ''
        }
        if purpose == 'command':
            response['input_data_type'] = self.command_data_type
        elif purpose == 'state':
            response['input_data_type'] = self.state_data_type
        elif purpose == 'measure':
            response['input_data_type'] = self.measure_data_type

        return response


class PackModel(RtuModel):
    def __init__(self, rtu, version):
        if rtu:
            self.__dict__ = copy.deepcopy(rtu.__dict__)
        else:
            RtuModel.__init__(self, None, None)

        self.pack_model = Pack.objects.filter(Version=version).first()
        self.st = re.sub(r'(?<={).+?(?=})', '', self.pack_model.ST)

    def pack(self, device_name, num_objects, rtu_purpose, internal_purpose, server_iteration, path):
        # Obtaining data
        pack_information = self.pack_decision_tree(rtu_purpose, internal_purpose)
        input_data = pack_information[0]
        input_data_type = pack_information[1]
        output_data = pack_information[2]
        output_data_type = pack_information[3]

        # Instance data
        pou_name = "Pack" + str(num_objects) + input_data_type + str(device_name) + rtu_purpose + str(server_iteration)

        # create file
        pack_object = open(path + "\\" + pou_name + ".EXP", "w+")

        # variable definition
        # Inputs
        input_str = variable_to_declaration(signal=input_data, num_objects=num_objects, data_type=input_data_type)
        var_input = self.declaration_input.format(input_str)

        # Outputs
        output_str = f"{output_data} : ARRAY [1..{num_objects}] OF {output_data_type};"
        var_output = self.declaration_output.format(output_str)

        # Declaration construction
        declaration = self.declaration_attributes + '\n'
        declaration += self.declaration_fb_header.format(pou_name) + '\n'
        declaration += var_input + '\n'
        declaration += var_output + '\n'
        declaration += self.declaration_end_tag + '\n'

        # Code construction
        code = ''
        for i in range(num_objects):
            code += self.st.format(output_data, i + 1, f"{input_data}{i + 1}") + '\n'
        code += self.code_end_tag

        # Writing the pou
        pack_object.write(declaration + code)

        # closing file
        pack_object.close()

        return pou_name


class CheckModel(RtuModel):
    def __init__(self, rtu, version):
        if rtu:
            self.__dict__ = copy.deepcopy(rtu.__dict__)
        else:
            RtuModel.__init__(self, None, None)

        self.check_model = Check.objects.filter(Version=version).first()
        self.iterator = self.check_model.Iterator
        self.iterator_data_type = self.check_model.IteratorDataType
        self.last_values = self.check_model.LastValues
        self.last_values_data_type = self.check_model.LastValuesDataType
        self.st = re.sub(r'(?<={).+?(?=})', '', self.check_model.ST)

    def check(self, device_name, num_objects, purpose, server_iteration, path):
        check_information = self.check_decision_tree(purpose)
        input_data = self.signals
        input_data_type = check_information['input_data_type']
        output_data = self.check_changes
        output_data_type = self.check_changes_data_type

        # Instance data
        pou_name = "Check" + str(num_objects) + input_data_type + str(device_name) + purpose + str(server_iteration)

        # create file
        check_object = open(path + "\\" + pou_name + ".EXP", "w+")

        # variable definition
        # Inputs
        input_str = f"{input_data} : ARRAY [1..{num_objects}] OF {input_data_type};" + '\n'
        input_str += f"{self.first_cycle} : {self.first_cycle_data_type};"
        var_input = self.declaration_input.format(input_str)

        # Outputs
        output_str = f"{output_data} : ARRAY [1..{num_objects}] OF {output_data_type};"
        var_output = self.declaration_output.format(output_str)

        # Internals
        internal_str = f"{self.iterator} : {self.iterator_data_type};" + '\n'
        internal_str += f"{self.last_values} : ARRAY [1..{num_objects}] OF {input_data_type};"
        var_internal = self.declaration_internal.format(internal_str)

        # Declaration construction
        declaration = self.declaration_attributes + '\n'
        declaration += self.declaration_fb_header.format(pou_name) + '\n'
        declaration += var_input + '\n'
        declaration += var_output + '\n'
        declaration += var_internal + '\n'
        declaration += self.declaration_end_tag + '\n'

        # Code construction
        code = self.st.format(
            self.iterator, num_objects,
            self.first_cycle,
            self.last_values, self.iterator, input_data, self.iterator,
            input_data, self.iterator, self.last_values, self.iterator,
            output_data, self.iterator,
            output_data, self.iterator,
            self.last_values, input_data
        )
        code += '\n' + self.code_end_tag

        # Writing the pou
        check_object.write(declaration + code)

        # Closing file
        check_object.close()

        return pou_name


class MapModel(RtuModel):
    def __init__(self, rtu, version):
        if rtu:
            self.__dict__ = copy.deepcopy(rtu.__dict__)
        else:
            RtuModel.__init__(self, None, None)

        self.map_model = Map.objects.filter(Version=version).first()
        self.st = re.sub(r'(?<={).+?(?=})', '', self.map_model.ST)

    def map(self, device_name, num_objects, purpose, server_iteration, path):
        # Obtaining data
        map_information = self.map_decision_tree(purpose)
        input_data = map_information[0]
        input_data_type = map_information[1]
        output_data = map_information[2]
        output_data_type = map_information[3]

        # Instance data
        pou_name = "Map" + str(num_objects) + input_data_type + str(device_name) + purpose + str(server_iteration)

        # create file
        map_object = open(path + "\\" + pou_name + ".EXP", "w+")

        # Variable declaration
        # Inputs
        input_str = f"{self.action} : {self.action_data_type};" + '\n'
        input_str += f"{self.state_loc_rem} : {self.loc_rem_state_data_type};" + '\n'
        input_str += variable_to_declaration(signal=input_data, num_objects=num_objects, data_type=input_data_type) + '\n'
        if purpose != 'measure':
            input_str += variable_to_declaration(signal=self.trigger_changes, num_objects=num_objects, data_type=self.trigger_changes_data_type) + '\n'
            input_str += variable_to_declaration(signal=self.check_changes, num_objects=num_objects, data_type=self.check_changes_data_type)
        var_input = self.declaration_input.format(input_str)

        # Outputs
        output_str = variable_to_declaration(signal=output_data, num_objects=num_objects, data_type=output_data_type)
        var_output = self.declaration_output.format(output_str)

        # Declaration construction
        declaration = self.declaration_attributes + '\n'
        declaration += self.declaration_fb_header.format(pou_name) + '\n'
        declaration += var_input + '\n'
        declaration += var_output + '\n'
        declaration += self.declaration_end_tag + '\n'

        # Code construction
        code = ""
        if purpose == 'measure':
            for i in range(num_objects):
                code += f"{output_data}{i + 1} := {input_data}{i + 1};" + '\n'
        else:
            for i in range(num_objects):
                code += f"IF {self.trigger_changes}{i + 1} OR {self.check_changes}{i + 1} THEN" + '\n'
                code += f"{output_data}{i + 1} := {input_data}{i + 1};" + '\n'
                code += "END_IF" + '\n'

        code = self.st.format(
            self.state_loc_rem, self.state_loc_rem, self.action,
            code
        )
        code += '\n' + self.code_end_tag

        # Writing the pou
        map_object.write(declaration + code)

        # Closing file
        map_object.close()

        return pou_name


class RiseModel(RtuModel):
    def __init__(self, rtu, version):
        if rtu:
            self.__dict__ = copy.deepcopy(rtu.__dict__)
        else:
            RtuModel.__init__(self, None, None)

        self.rise_model = RiseToTrigger.objects.filter(Version=version).first()
        self.last_rise = self.rise_model.LastRise
        self.last_rise_data_type = self.rise_model.LastRiseDataType
        self.iterator = self.rise_model.Iterator
        self.iterator_data_type = self.rise_model.IteratorDataType
        self.st = re.sub(r'(?<={).+?(?=})', '', self.rise_model.ST)

    def rise(self, device_name, num_objects, purpose, server_iteration, path):
        # Obtaining data
        input_data = self.rise_changes
        input_data_type = self.rise_changes_data_type
        output_data = self.trigger_changes
        output_data_type = self.trigger_changes_data_type

        # Instance data
        pou_name = "Rise" + str(num_objects) + input_data_type + str(device_name) + purpose + str(server_iteration)

        # create file
        rise_object = open(path + "\\" + pou_name + ".EXP", "w+")

        # variable definition
        # Inputs
        input_str = f"{input_data} : ARRAY [1..{num_objects}] OF {input_data_type}"
        var_input = self.declaration_input.format(input_str)

        # Outputs
        output_str = f"{output_data} : ARRAY [1..{num_objects}] OF {output_data_type};"
        var_output = self.declaration_output.format(output_str)

        # Internals
        internal_str = f"{self.last_rise} : ARRAY [1..{num_objects}] OF {self.last_rise_data_type};" + '\n'
        internal_str += f"{self.iterator} : {self.iterator_data_type};"
        var_internal = self.declaration_internal.format(internal_str)

        # Declaration construction
        declaration = ''
        declaration += self.declaration_attributes + '\n'
        declaration += self.declaration_fb_header.format(pou_name) + '\n'
        declaration += var_input + '\n'
        declaration += var_output + '\n'
        declaration += var_internal + '\n'
        declaration += self.declaration_end_tag + '\n'

        # Code construction
        code = self.st.format(
            self.iterator, num_objects,
            input_data, self.iterator, self.last_rise, self.iterator,
            output_data, self.iterator,
            self.last_rise, self.iterator, input_data, self.iterator,
            output_data, self.iterator
        )
        code += '\n' + self.code_end_tag

        # Writing the pou
        rise_object.write(declaration + code)

        # Closing file
        rise_object.close()

        return pou_name


class SaveModel(RtuModel):
    def __init__(self, rtu, version):
        if rtu:
            self.__dict__ = copy.deepcopy(rtu.__dict__)
        else:
            RtuModel.__init__(self, None, None)

        self.save_model = Save.objects.filter(Version=version).first()
        self.reason = self.save_model.Reason
        self.reason_data_type = self.save_model.ReasonDataType
        self.reason_init_val = self.save_model.ReasonInitVal
        self.time = self.save_model.Time
        self.time_data_type = self.save_model.TimeDataType
        self.offset = self.save_model.Offset
        self.offset_data_type = self.save_model.OffsetDataType
        self.iterator = self.save_model.Iterator
        self.iterator_data_type = self.save_model.IteratorDataType
        self.power_on_prefix = self.save_model.PowerOnPrefix
        self.power_on_prefix_data_type = self.save_model.PowerOnPrefixDataType
        self.power_on_prefix_init_val = self.save_model.PowerOnPrefixInitVal
        self.prefix_under_line = self.save_model.PrefixUnderLine
        self.prefix_under_line_data_type = self.save_model.PrefixUnderLineDataType
        self.prefix_under_line_init_val = self.save_model.PrefixUnderLineInitVal
        self.delimiter = self.save_model.Delimiter
        self.delimiter_data_type = self.save_model.DelimiterDataType
        self.delimiter_init_val = self.save_model.DelimiterInitVal
        self.object_value = self.save_model.ObjectValue
        self.object_value_data_type = self.save_model.ObjectValueDataType
        self.prefix = self.save_model.Prefix
        self.prefix_data_type = self.save_model.PrefixDataType
        self.file = self.save_model.File
        self.file_data_type = self.save_model.FileDataType
        self.close = self.save_model.Close
        self.close_data_type = self.save_model.CloseDataType
        self.new_line = self.save_model.NewLine
        self.new_line_data_type = self.save_model.NewLineDataType
        self.new_line_init_val = self.save_model.NewLineInitVal
        self.hysteresis = self.save_model.Hysteresis
        self.hysteresis_data_type = self.save_model.HysteresisDataType
        self.last_values = self.save_model.LastValues
        self.last_values_data_type = self.save_model.LastValuesDataType
        self.st = re.sub(r'(?<={).+?(?=})', '', self.save_model.ST)

    def save(self, device_name, num_objects, purpose, server_iteration, path):
        # Obtaining data
        save_information = self.save_decision_tree(purpose)
        input_data = self.signals
        input_data_type = save_information['input_data_type']

        # Instance data
        pou_name = "Save" + str(num_objects) + input_data_type + str(device_name) + purpose + str(server_iteration)

        # create file
        save_object = open(path + "\\" + pou_name + ".EXP", "w+")

        # Variable definition
        # Inputs
        input_str = f"{self.first_cycle} : {self.first_cycle_data_type};" + '\n'
        input_str += f"{self.sequence_order} : {self.sequence_order_data_type};" + '\n'
        input_str += f"{self.protocol} : {self.protocol_data_type};" + '\n'
        input_str += f"{self.state_loc_rem} : {self.state_loc_rem_data_type};" + '\n'
        input_str += f"{self.action} : {self.action_data_type};" + '\n'
        input_str += f"{input_data} : ARRAY [1..{num_objects}] OF {input_data_type};" + '\n'
        input_str += f"{self.names} : ARRAY [1..{num_objects}] OF {self.names_data_type};" + '\n'
        input_str += f"{self.check_changes} : ARRAY [1..{num_objects}] OF {self.check_changes_data_type};" + '\n'
        input_str += f"{self.saves} : ARRAY [1..{num_objects}] OF {self.saves_data_type};" + '\n'
        var_input = self.declaration_input.format(input_str)

        # Internals
        internal_str = f"{self.reason} : {self.reason_data_type} := {self.reason_init_val};" + '\n'
        internal_str += f"{self.time} : {self.time_data_type};" + '\n'
        internal_str += f"{self.offset} : {self.offset_data_type};" + '\n'
        internal_str += f"{self.iterator} : {self.iterator_data_type};" + '\n'
        internal_str += f"{self.power_on_prefix} : {self.power_on_prefix_data_type} := {self.power_on_prefix_init_val};" + '\n'
        internal_str += f"{self.prefix_under_line} : {self.prefix_under_line_data_type} := {self.prefix_under_line_init_val};" + '\n'
        internal_str += f"{self.delimiter} : {self.delimiter_data_type} := {self.delimiter_init_val};" + '\n'
        internal_str += f"{self.object_value} : {self.object_value_data_type};" + '\n'
        internal_str += f"{self.prefix} : {self.prefix_data_type};" + '\n'
        internal_str += f"{self.file} : {self.file_data_type};" + '\n'
        internal_str += f"{self.close} : {self.close_data_type};" + '\n'
        internal_str += f"{self.new_line} : {self.new_line_data_type} := {self.new_line_init_val};" + '\n'

        # Obtaining hysteresis derivatives
        hysteresis_condition = ""
        internal_input_code = ""
        hysteresis_code_end_tag = ""
        if input_data_type == "WORD":
            hysteresis = Obj35mMeTe.objects.filter(DeviceName=device_name).first().Hysteresis
            if hysteresis:
                internal_str += f"{self.hysteresis} : ARRAY[1..{num_objects}] OF {self.hysteresis_data_type} := [{hysteresis}];"
                internal_str += f"{self.last_values} : ARRAY[1..{num_objects}] OF {self.last_values_data_type};"
                hysteresis_condition = f"IF ({input_data}[{self.iterator}] > ({self.last_values}" \
                                       f"[{self.iterator}] + (({self.hysteresis}[{self.iterator}] / 100) * " \
                                       f"{self.last_values}[{self.iterator}] ))) OR ({input_data}" \
                                       f"[{self.iterator}] < ({self.last_values}[{self.iterator}] - " \
                                       f"(({self.hysteresis}[{self.iterator}] / 100) * {self.last_values}" \
                                       f"[{self.iterator}]))) THEN"
                internal_input_code = f"{self.last_values}[{self.iterator}] := {input_data}[{self.iterator}];"
                hysteresis_code_end_tag = "END_IF"

        # Writing internals in their module
        var_internal = self.declaration_internal.format(internal_str)

        # Declaration construction
        declaration = self.declaration_attributes + '\n'
        declaration += self.declaration_f_header.format(pou_name) + '\n'
        declaration += var_input + '\n'
        declaration += var_internal + '\n'
        declaration += self.declaration_end_tag + '\n'

        # Code construction
        code = self.st.format(
            self.file,
            self.time,
            self.offset, self.sequence_order, num_objects,
            self.protocol, self.protocol, self.prefix_under_line,
            self.prefix, self.protocol, self.sequence_order_data_type, self.sequence_order,
            self.first_cycle,
            self.iterator, num_objects,
            self.saves, self.iterator,
            internal_input_code,
            input_data_type, input_data, self.iterator,
            self.file, self.time, self.time,
            self.file, self.delimiter, self.delimiter,
            self.file, self.prefix, self.prefix,
            self.file, self.delimiter, self.delimiter,
            self.file, self.power_on_prefix, self.power_on_prefix,
            self.file, self.names, self.iterator, self.names, self.iterator,
            self.file, self.delimiter, self.delimiter,
            self.file, self.object_value, self.object_value,
            self.file, self.new_line, self.new_line,
            self.iterator, num_objects,
            self.saves, self.iterator,
            self.check_changes, self.iterator,
            hysteresis_condition,
            internal_input_code,
            input_data_type, input_data, self.iterator,
            self.file, self.time, self.time,
            self.file, self.delimiter, self.delimiter,
            self.file, self.prefix, self.prefix,
            self.file, self.delimiter, self.delimiter,
            self.file, self.power_on_prefix, self.power_on_prefix,
            self.file, self.names, self.iterator, self.names, self.iterator,
            self.file, self.delimiter, self.delimiter,
            self.file, self.object_value, self.object_value,
            self.file, self.new_line, self.new_line,
            hysteresis_code_end_tag,
            self.close, self.file,
            pou_name
        )

        code += '\n' + self.code_end_tag

        # Writing the pou
        save_object.write(declaration + code)

        # Closing file
        save_object.close()

        return pou_name


class SboModel(RtuModel):
    def __init__(self, rtu, version):
        if rtu:
            self.__dict__ = copy.deepcopy(rtu.__dict__)
        else:
            RtuModel.__init__(self, None, None)

        self.sbo_model = Sbo.objects.filter(Version=version).first()
        self.error_stat_internal = self.sbo_model.ErrorStatInternal
        self.error_stat_internal_data_type = self.sbo_model.ErrorStatInternalDataType
        self.flag = self.sbo_model.Flag
        self.flag_data_type = self.sbo_model.FlagDataType
        self.st_body = re.sub(r'(?<={).+?(?=})', '', self.sbo_model.STBody)
        self.st_core = re.sub(r'(?<={).+?(?=})', '', self.sbo_model.STCore)

    def sbo(self, device_name, num_objects, purpose, server_iteration, path):
        # Obtaining data
        input_data_type = self.check_changes_data_type

        # Instance data
        pou_name = "Sbo" + str(num_objects) + input_data_type + str(device_name) + purpose + str(server_iteration)

        # create file
        sbo_object = open(path + "\\" + pou_name + ".EXP", "w+")

        # Variable declaration
        # Inputs
        input_str = f"{self.state_loc_rem} : {self.state_loc_rem_data_type};" + '\n'
        input_str += variable_to_declaration(signal=self.trigger_changes, num_objects=num_objects, data_type=self.trigger_changes_data_type) + '\n'
        input_str += variable_to_declaration(signal=self.status, num_objects=int(num_objects / 2), data_type=self.status_data_type) + '\n'
        var_input = self.declaration_input.format(input_str)

        # Outputs
        output_str = variable_to_declaration(signal=self.select, num_objects=int(num_objects / 2), data_type=self.select_data_type) + '\n'
        output_str += variable_to_declaration(signal=self.execute, num_objects=int(num_objects / 2), data_type=self.execute_data_type) + '\n'
        output_str += f"{self.error} : {self.error_data_type};"
        var_output = self.declaration_output.format(output_str)

        # Internals
        internal_str = f"{self.error_stat_internal} : {self.error_stat_internal_data_type};"
        internal_str += variable_to_declaration(signal=self.flag, num_objects=int(num_objects / 2), data_type=self.flag_data_type) + '\n'
        var_internal = self.declaration_internal.format(internal_str)

        # Declaration construction
        declaration = self.declaration_attributes + '\n'
        declaration += self.declaration_fb_header.format(pou_name) + '\n'
        declaration += var_input + '\n'
        declaration += var_output + '\n'
        declaration += var_internal + '\n'
        declaration += self.declaration_end_tag + '\n'

        # Code construction
        code_core = ''
        for s in range(int(num_objects / 2)):
            code_core += self.st_core.format(
                f"{self.flag}{s + 1}",
                f"{self.trigger_changes}{(2 * s) + 1}", f"{self.trigger_changes}{(2 * s) + 2}",
                f"{self.select}{s + 1}",
                f"{self.flag}{s + 1}",
                f"{self.flag}{s + 1}",
                f"{self.status}{s + 1}",
                f"{self.select}{s + 1}",
                f"{self.select}{s + 1}",
                f"{self.execute}{s + 1}",
                f"{self.execute}{s + 1}",
                f"{self.flag}{s + 1}",
                self.error_stat_internal,
                f"{self.execute}{s + 1}",
                f"{self.select}{s + 1}",
                f"{self.flag}{s + 1}",
                self.error_stat_internal,
                f"{self.execute}{s + 1}",
                f"{self.select}{s + 1}",
                f"{self.flag}{s + 1}",
                self.error_stat_internal,
            ) + "\n\n"

        code = self.st_body.format(
            self.error_stat_internal,
            self.state_loc_rem,
            self.error, self.error_stat_internal,
            code_core,
            self.error, self.error_stat_internal
        )
        code += '\n' + self.code_end_tag

        # Writing the pou
        sbo_object.write(declaration + code)

        # Closing file
        sbo_object.close()

        return pou_name


class HandlerModel(RtuModel):
    def __init__(self, rtu, version):
        if rtu:
            self.__dict__ = copy.deepcopy(rtu.__dict__)
        else:
            RtuModel.__init__(self, None, None)

        self.handler_model = Handler.objects.filter(Version=version).first()
        self.error_description = self.handler_model.ErrorDescription
        self.error_description_data_type = self.handler_model.ErrorDescriptionDataType
        self.st = re.sub(r'(?<={).+?(?=})', '', self.handler_model.ST)

    def handler(self, device_name, server_iteration, path):
        # Instance data
        pou_name = "Handler" + str(device_name) + str(server_iteration)

        # create file
        handler_object = open(path + "\\" + pou_name + ".EXP", "w+")

        # Variable declaration
        # Inputs
        input_str = f"{self.error} : {self.error_data_type};" + '\n'

        # Internals
        internal_str = f"{self.error_description} : {self.error_description};" + '\n'

        # Declaration construction
        declaration = self.declaration_attributes + '\n'
        declaration += self.declaration_f_header.format(pou_name) + '\n'
        declaration += self.declaration_input.format(input_str) + '\n'
        declaration += self.declaration_internal.format(internal_str) + '\n'
        declaration += self.declaration_end_tag + '\n'

        # Code construction
        code = self.st.format(
            self.error,
            self.error,
            self.error_description,
            self.error_description,
            self.error_description,
            self.error_description,
            self.error_description,
            pou_name
        )
        code += '\n' + self.code_end_tag

        # Writing the pou
        handler_object.write(declaration + code)

        return pou_name
