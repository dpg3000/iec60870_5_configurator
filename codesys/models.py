from django.db import models
import copy
from support_functions import variable_to_declaration, dummy_to_declaration
from server_parts.models import Obj35mMeTe
import pou
import re

# Pou versions menu
user_prg_version = 'userprgv0'
pack_loc_rem_version = 'packlocremv0'
check_loc_rem_version = 'checklocremv0'
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
    AssignInputHeader = models.TextField(default="")
    InputUnit = models.TextField(default="")
    FunctionBlockOutputHeader = models.TextField(default="")
    FunctionOutputHeader = models.TextField(default="")
    OutputUnit = models.TextField(default="")
    CodeEndTag = models.CharField(max_length=255, default="")

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(FBDTemplate, self).save()
        pou.fbd_model = FunctionBlockDiagramModel()
        pou.user_prg_model = UserPrgModel(pou.fbd_model, user_prg_version)
        pou.pack_loc_rem_model = PackLocRemModel(pou.user_prg_model, pack_loc_rem_version)
        pou.check_loc_rem_model = CheckLocRemModel(pou.user_prg_model, check_loc_rem_version)
        pou.device_model = DeviceModel(pou.user_prg_model, device_version)
        pou.rtu_model = RtuModel(pou.device_model, rtu_version)
        pou.pack_model = PackModel(pou.rtu_model, pack_version)
        pou.check_model = CheckModel(pou.rtu_model, check_version)
        pou.map_model = MapModel(pou.rtu_model, map_version)
        pou.rise_model = RiseModel(pou.rtu_model, rise_version)
        pou.save_model = SaveModel(pou.rtu_model, save_version)
        pou.sbo_model = SboModel(pou.rtu_model, sbo_version)
        pou.handler_model = HandlerModel(pou.rtu_model, handler_version)

    class Meta:
        verbose_name_plural = "fbd_template"


class UserPrg(models.Model):
    Version = models.CharField(max_length=255, default="")
    ProgramHeader = models.CharField(max_length=255, default="")
    ProgramEndTag = models.CharField(max_length=255, default="")
    FirstCycle = models.CharField(max_length=255, default="")
    FirstCycleDataType = models.CharField(max_length=255, default="")
    FirstCycleInitVal = models.CharField(max_length=255, default="")
    MaskLocRem = models.CharField(max_length=255, default="")
    MaskLocRemDataType = models.CharField(max_length=255, default="")
    StateLocRem = models.CharField(max_length=255, default="")
    StateLocRemDataType = models.CharField(max_length=255, default="")
    DummyMeasure = models.CharField(max_length=255, default="")
    DummyMeasureDataType = models.CharField(max_length=255, default="")
    DummyMeasureOutput = models.CharField(max_length=255, default="")
    DummyMeasureOutputDataType = models.CharField(max_length=255, default="")
    DummyState = models.CharField(max_length=255, default="")
    DummyStateDataType = models.CharField(max_length=255, default="")
    DummyStateOutput = models.CharField(max_length=255, default="")
    DummyStateOutputDataType = models.CharField(max_length=255, default="")
    DummyCommand = models.CharField(max_length=255, default="")
    DummyCommandDataType = models.CharField(max_length=255, default="")
    DummyCommandOutput = models.CharField(max_length=255, default="")
    DummyCommandOutputDataType = models.CharField(max_length=255, default="")
    DummyStatus = models.CharField(max_length=255, default="")
    DummyStatusDataType = models.CharField(max_length=255, default="")
    DummySelect = models.CharField(max_length=255, default="")
    DummySelectDataType = models.CharField(max_length=255, default="")
    DummyExecute = models.CharField(max_length=255, default="")
    DummyExecuteDataType = models.CharField(max_length=255, default="")

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(UserPrg, self).save()
        pou.user_prg_model = UserPrgModel(pou.fbd_model, user_prg_version)
        pou.pack_loc_rem_model = PackLocRemModel(pou.user_prg_model, pack_loc_rem_version)
        pou.check_loc_rem_model = CheckLocRemModel(pou.user_prg_model, check_loc_rem_version)
        pou.device_model = DeviceModel(pou.user_prg_model, device_version)
        pou.rtu_model = RtuModel(pou.device_model, rtu_version)
        pou.pack_model = PackModel(pou.rtu_model, pack_version)
        pou.check_model = CheckModel(pou.rtu_model, check_version)
        pou.map_model = MapModel(pou.rtu_model, map_version)
        pou.rise_model = RiseModel(pou.rtu_model, rise_version)
        pou.save_model = SaveModel(pou.rtu_model, save_version)
        pou.sbo_model = SboModel(pou.rtu_model, sbo_version)
        pou.handler_model = HandlerModel(pou.rtu_model, handler_version)

    def __str__(self):
        return self.Version

    class Meta:
        verbose_name_plural = "user_prg"


class PackLocRem(models.Model):
    Version = models.CharField(max_length=255)
    LocRemInput = models.CharField(max_length=255, default="")
    LocRemInputDataType = models.CharField(max_length=255, default="")
    LocRemOutput = models.CharField(max_length=255, default="")
    LocRemOutputDataType = models.CharField(max_length=255, default="")
    ST = models.TextField(default="")

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(PackLocRem, self).save()
        pou.pack_loc_rem_model = PackLocRemModel(pou.user_prg_model, pack_loc_rem_version)

    def __str__(self):
        return self.Version

    class Meta:
        verbose_name_plural = "pack_loc_rem"


class CheckLocRem(models.Model):
    Version = models.CharField(max_length=255)
    Iterator = models.CharField(max_length=255, default="")
    IteratorDataType = models.CharField(max_length=255, default="")
    ST = models.TextField(default="")

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(CheckLocRem, self).save()
        pou.check_loc_rem_model = CheckLocRemModel(pou.user_prg_model, check_loc_rem_version)

    def __str__(self):
        return self.Version

    class Meta:
        verbose_name_plural = "check_loc_rem"


class Device(models.Model):
    Version = models.CharField(max_length=255, default="")
    SequenceOrder = models.CharField(max_length=255, default="")
    SequenceOrderDataType = models.CharField(max_length=255, default="")
    Protocol = models.CharField(max_length=255, default="")
    ProtocolDataType = models.CharField(max_length=255, default="")
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
        pou.rtu_model = RtuModel(pou.device_model, rtu_version)
        pou.pack_model = PackModel(pou.rtu_model, pack_version)
        pou.check_model = CheckModel(pou.rtu_model, check_version)
        pou.map_model = MapModel(pou.rtu_model, map_version)
        pou.rise_model = RiseModel(pou.rtu_model, rise_version)
        pou.save_model = SaveModel(pou.rtu_model, save_version)
        pou.sbo_model = SboModel(pou.rtu_model, sbo_version)
        pou.handler_model = HandlerModel(pou.rtu_model, handler_version)

    def __str__(self):
        return self.Version

    class Meta:
        verbose_name_plural = "device"


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
        pou.pack_model = PackModel(pou.rtu_model, pack_version)
        pou.check_model = CheckModel(pou.rtu_model, check_version)
        pou.map_model = MapModel(pou.rtu_model, map_version)
        pou.rise_model = RiseModel(pou.rtu_model, rise_version)
        pou.save_model = SaveModel(pou.rtu_model, save_version)
        pou.sbo_model = SboModel(pou.rtu_model, sbo_version)
        pou.handler_model = HandlerModel(pou.rtu_model, handler_version)

    def __str__(self):
        return self.Version

    class Meta:
        verbose_name_plural = "rtu"


class Pack(models.Model):
    Version = models.CharField(max_length=255)
    ST = models.TextField(default="")

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(Pack, self).save()
        pou.pack_model = PackModel(pou.rtu_model, pack_version)

    def __str__(self):
        return self.Version

    class Meta:
        verbose_name_plural = "pack"


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

    class Meta:
        verbose_name_plural = "check"


class Map(models.Model):
    Version = models.CharField(max_length=255)
    ST = models.TextField(default="")

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(Map, self).save()
        pou.pack_model = PackModel(pou.rtu_model, map_version)

    def __str__(self):
        return self.Version

    class Meta:
        verbose_name_plural = "map"


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

    class Meta:
        verbose_name_plural = "rise_to_trigger"


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

    class Meta:
        verbose_name_plural = "save"


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

    class Meta:
        verbose_name_plural = "sbo"


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

    class Meta:
        verbose_name_plural = "handler"


class FunctionBlockDiagramModel:
    def __init__(self):
        self.function_block_diagram_template = FBDTemplate.objects.first()
        self.declaration_attributes = self.function_block_diagram_template.DeclarationAttributes
        self.declaration_fb_header = self.function_block_diagram_template.DeclarationFBHeader
        self.declaration_f_header = self.function_block_diagram_template.DeclarationFHeader
        self.declaration_input = self.function_block_diagram_template.DeclarationInput
        self.declaration_output = self.function_block_diagram_template.DeclarationOutput
        self.declaration_internal = self.function_block_diagram_template.DeclarationInternal
        self.declaration_end_tag = self.function_block_diagram_template.DeclarationEndTag
        self.header = self.function_block_diagram_template.Header
        self.function_block_input_header = self.function_block_diagram_template.FunctionBlockInputHeader
        self.function_input_header = self.function_block_diagram_template.FunctionInputHeader
        self.assign_input_header = self.function_block_diagram_template.AssignInputHeader
        self.input_unit = self.function_block_diagram_template.InputUnit
        self.function_block_output_header = self.function_block_diagram_template.FunctionBlockOutputHeader
        self.function_output_header = self.function_block_diagram_template.FunctionOutputHeader
        self.output_unit = self.function_block_diagram_template.OutputUnit
        self.code_end_tag = self.function_block_diagram_template.CodeEndTag


class UserPrgModel(FunctionBlockDiagramModel):
    # Copy constructor implementation
    def __init__(self, fbd, version):
        if fbd:
            self.__dict__ = copy.deepcopy(fbd.__dict__)
        else:
            FunctionBlockDiagramModel.__init__(self)

        self.user_prg_model = UserPrg.objects.filter(Version=version).first()
        self.program_header = self.user_prg_model.ProgramHeader
        self.program_end_tag = self.user_prg_model.ProgramEndTag
        self.first_cycle = self.user_prg_model.FirstCycle
        self.first_cycle_data_type = self.user_prg_model.FirstCycleDataType
        self.first_cycle_init_val = self.user_prg_model.FirstCycleInitVal
        self.mask_loc_rem = self.user_prg_model.MaskLocRem
        self.mask_loc_rem_data_type = self.user_prg_model.MaskLocRemDataType
        self.state_loc_rem = self.user_prg_model.StateLocRem
        self.state_loc_rem_data_type = self.user_prg_model.StateLocRemDataType
        self.dummy_measure = self.user_prg_model.DummyMeasure
        self.dummy_measure_data_type = self.user_prg_model.DummyMeasureDataType
        self.dummy_measure_output = self.user_prg_model.DummyMeasureOutput
        self.dummy_measure_output_data_type = self.user_prg_model.DummyMeasureOutputDataType
        self.dummy_state = self.user_prg_model.DummyState
        self.dummy_state_data_type = self.user_prg_model.DummyStateDataType
        self.dummy_state_output = self.user_prg_model.DummyStateOutput
        self.dummy_state_output_data_type = self.user_prg_model.DummyStateOutputDataType
        self.dummy_command = self.user_prg_model.DummyCommand
        self.dummy_command_data_type = self.user_prg_model.DummyCommandDataType
        self.dummy_command_output = self.user_prg_model.DummyCommandOutput
        self.dummy_command_output_data_type = self.user_prg_model.DummyCommandOutputDataType
        self.dummy_status = self.user_prg_model.DummyStatus
        self.dummy_status_data_type = self.user_prg_model.DummyStatusDataType
        self.dummy_select = self.user_prg_model.DummySelect
        self.dummy_select_data_type = self.user_prg_model.DummySelectDataType
        self.dummy_execute = self.user_prg_model.DummyExecute
        self.dummy_execute_data_type = self.user_prg_model.DummyExecuteDataType
        self.dev_iteration = 0

    def user_prg(self, device_list, num_objects, pack_loc_rem, check_loc_rem, server_iteration, path):
        # Instance data
        pou_name = "USER_PRG"

        # create file
        user_prg_object = open(path + "\\" + pou_name + ".EXP", "w+")

        # variable definition
        # Internal variables
        internal_str = ''
        internal_str += f"{self.first_cycle}    : {self.first_cycle_data_type} := {self.first_cycle_init_val};" + '\n\t'
        internal_str += f"{self.mask_loc_rem}   : ARRAY [1..{num_objects}] OF {self.mask_loc_rem_data_type};" + '\n\t'
        internal_str += f"{self.state_loc_rem}  : ARRAY [1..{num_objects - 1}] OF {self.state_loc_rem_data_type};"
        internal_str += '\n\t'

        # Internal dummies
        for device in device_list:
            for k in range(device['quantity']):
                internal_str += f"(*{device['name']}_{k}*)" + '\n\t'
                # Measurements
                if device['measurements']:
                    internal_str += dummy_to_declaration(
                        signal=f"{self.dummy_measure}_{device['name']}",
                        dev=self.dev_iteration,
                        size=len(device['measurements'][k]),
                        data_type=self.dummy_measure_data_type
                    ) + '\n\t'
                # States
                if device['states']:
                    internal_str += dummy_to_declaration(
                        signal=f"{self.dummy_state}_{device['name']}",
                        dev=self.dev_iteration,
                        size=len(device['states'][k]),
                        data_type=self.dummy_state_data_type
                    ) + '\n\t'
                # Commands
                if device['commands']:
                    internal_str += dummy_to_declaration(
                        signal=f"{self.dummy_command_output}_{device['name']}",
                        dev=self.dev_iteration,
                        size=len(device['commands'][k]),
                        data_type=self.dummy_command_output_data_type
                    ) + '\n\t'
                    # SBO | DO
                    if device['operation'] == 'SBO':
                        # Status
                        internal_str += dummy_to_declaration(
                            signal=f"{self.dummy_status}_{device['name']}",
                            dev=self.dev_iteration,
                            size=int(len(device['commands'][k]) / 2),
                            data_type=self.dummy_status_data_type
                        ) + '\n\t'
                        # Select
                        internal_str += dummy_to_declaration(
                            signal=f"{self.dummy_select}_{device['name']}",
                            dev=self.dev_iteration,
                            size=int(len(device['commands'][k]) / 2),
                            data_type=self.dummy_select_data_type
                        ) + '\n\t'
                        # Execute
                        internal_str += dummy_to_declaration(
                            signal=f"{self.dummy_execute}_{device['name']}",
                            dev=self.dev_iteration,
                            size=int(len(device['commands'][k]) / 2),
                            data_type=self.dummy_execute_data_type
                        ) + '\n\t'
                self.dev_iteration += 1
        self.dev_iteration = 0

        # instances
        internal_str += f"inst0{pack_loc_rem}   : {pack_loc_rem};" + '\n\t'
        internal_str += f"inst0{check_loc_rem}  : {check_loc_rem};" + '\n\t'

        total_networks = 3  # pack + check + clearing
        for device in device_list:
            for i in range(device['quantity']):
                internal_str += f"inst{i}{device['name']} : {device['name']};" + '\n\t'
            total_networks += device['quantity']

        # Declaration construction
        declaration = self.declaration_attributes + '\n'
        declaration += self.program_header.format(pou_name=pou_name) + '\n'
        declaration += self.declaration_internal.format(internal=internal_str) + '\n'
        declaration += self.declaration_end_tag + '\n'
        user_prg_object.write(declaration)

        # Code construction
        user_prg_object.write(self.header.format(size=str(total_networks)) + '\n')

        # instantiation
        # Pack
        self._pack_loc_rem_fbd(pack_loc_rem, num_objects, user_prg_object)

        # Check
        self._check_loc_rem_fbd(check_loc_rem, user_prg_object)

        # Devices
        for device in device_list:
            self._device_fbd(device, server_iteration, user_prg_object)

        # First Cycle clearing
        self._assign(self.first_cycle, "FALSE", user_prg_object)

        # Final tag
        user_prg_object.write(self.program_end_tag + '\n')

        # Closing file
        user_prg_object.close()

        # clearing device iterations
        self.dev_iteration = 0

    def _pack_loc_rem_fbd(self, instance, num_objects, file):
        # Inputs
        ####################################################################

        # Input header
        fbd_str = self.function_block_input_header.format(
            title='',
            instance=f"inst0{instance}",
            size=str(num_objects)
        ) + '\n'

        # Input unit
        for i in range(num_objects):
            fbd_str += self.input_unit.format(signal="_EMPTY") + '\n'

        # Outputs
        ####################################################################

        # Output header 1
        fbd_str += self.function_block_output_header.format(instance=instance, size="0") + '\n'

        # Output header 2
        fbd_str += self.function_block_output_header.format(instance="", size="1") + '\n'

        # Output unit
        fbd_str += self.output_unit.format(signal=self.mask_loc_rem) + '\n'

        # Writing the fbd
        file.write(fbd_str)

    def _check_loc_rem_fbd(self, instance, file):
        # Inputs
        ####################################################################

        # Input header
        fbd_str = self.function_block_input_header.format(title='', instance=f"inst0{instance}", size="1") + '\n'

        # Input unit
        fbd_str += self.input_unit.format(signal=self.mask_loc_rem) + '\n'

        # Outputs
        ####################################################################

        # Output header 1
        fbd_str += self.function_block_output_header.format(instance=instance, size="0") + '\n'

        # Output header 2
        fbd_str += self.function_block_output_header.format(instance="", size="1") + '\n'

        # Output unit
        fbd_str += self.output_unit.format(signal=self.state_loc_rem) + '\n'

        # Writing the fbd
        file.write(fbd_str)

    def _device_fbd(self, device, server_iteration, file):
        for i in range(device['quantity']):
            # Inputs
            ####################################################################

            # Input size
            control_inputs = 4
            rtu_inputs = 0
            if device['measurements']:
                rtu_inputs += 3 * len(device['measurements'][i])
            if device['states']:
                rtu_inputs += 4 * len(device['states'][i])
            if device['commands']:
                rtu_inputs += 4 * len(device['commands'][i])

                if device['operation'] == 'SBO':
                    rtu_inputs += int(len(device['commands'][i]) / 2)

            total_inputs = control_inputs + rtu_inputs

            # Input header
            fbd_str = self.function_block_input_header.format(
                title=f"Server_{server_iteration - 1}_{device['name']}_{i}",
                instance=f"inst{i}{device['name']}",
                size=total_inputs
            ) + '\n'

            ####################################################################

            # Control inputs
            fbd_str += self.input_unit.format(signal=self.first_cycle) + '\n'
            fbd_str += self.input_unit.format(signal=str(i)) + '\n'
            fbd_str += self.input_unit.format(signal=f"'{device['protocol']}'") + '\n'
            fbd_str += self.input_unit.format(signal=f"eState[{self.dev_iteration + 1}]") + '\n'

            ####################################################################

            # Measurements
            if device['measurements']:
                # signals
                for count in range(len(device['measurements'][i])):
                    fbd_str += self.input_unit.format(
                        signal=f"{self.dummy_measure}_{device['name']}_{self.dev_iteration}_{count + 1}"
                    ) + '\n'

                # saves
                for save in device['measurements'][i]:
                    fbd_str += self.input_unit.format(signal="TRUE") + '\n'

                # names
                for name in device['measurements_names'][i]:
                    fbd_str += self.input_unit.format(signal=f"'{name}'") + '\n'

            ####################################################################

            # States
            if device['states']:
                # signals
                for count in range(len(device['states'][i])):
                    fbd_str += self.input_unit.format(
                        signal=f"{self.dummy_state}_{device['name']}_{self.dev_iteration}_{count + 1}"
                    ) + '\n'

                # saves
                for save in device['states'][i]:
                    fbd_str += self.input_unit.format(signal="TRUE") + '\n'

                # names
                for name in device['states_names'][i]:
                    fbd_str += self.input_unit.format(signal=f"'{name}'") + '\n'

                # rises
                for count in range(len(device['states'][i])):
                    fbd_str += self.input_unit.format(signal="_EMPTY") + '\n'

            ####################################################################

            # Commands
            if device['commands']:
                # signals
                for command in device['commands'][i]:
                    fbd_str += self.input_unit.format(signal=command) + '\n'

                # saves
                for save in device['commands'][i]:
                    fbd_str += self.input_unit.format(signal="TRUE") + '\n'

                # names
                for name in device['commands_names'][i]:
                    fbd_str += self.input_unit.format(signal=f"'{name}'") + '\n'

                # triggers
                for trigger in device['commands_triggers'][i]:
                    fbd_str += self.input_unit.format(signal=trigger) + '\n'

                # status
                if device['operation'] == 'SBO':
                    for k in range(int(len(device['commands'][i]) / 2)):
                        fbd_str += self.input_unit.format(
                            signal=f"{self.dummy_status}_{device['name']}_{self.dev_iteration}_{k + 1}"
                        ) + '\n'

            # Outputs
            ####################################################################

            # Number of outputs
            rtu_outputs = 0

            if device['measurements']:
                rtu_outputs += len(device['measurements'][i])
            if device['states']:
                rtu_outputs += len(device['states'][i])
            if device['commands']:
                rtu_outputs += len(device['commands'][i])
                if device['operation'] == 'SBO':
                    rtu_outputs += 2 * int(len(device['commands'][i]) / 2)

            # Output header 1
            fbd_str += self.function_block_output_header.format(
                instance=device['name'],
                size=str(rtu_outputs - 1)
            ) + '\n'

            ####################################################################

            # Measurements
            if device['measurements']:
                for k in range(len(device['measurements'][i]) - 1):
                    fbd_str += self.output_unit.format(signal=device['measurements'][i][k + 1]) + '\n'

            ####################################################################

            # States
            if device['states']:
                if device['measurements']:
                    for state in device['states'][i]:
                        fbd_str += self.output_unit.format(signal=state) + '\n'
                else:
                    for k in range(len(device['states'][i]) - 1):
                        fbd_str += self.output_unit.format(signal=device['states'][i][k + 1]) + '\n'

            ####################################################################

            # Commands
            if device['commands']:
                if device['measurements'] or device['states']:
                    for k in range(len(device['commands'][i])):
                        fbd_str += self.output_unit.format(
                            signal=f"{self.dummy_command_output}_{device['name']}_{self.dev_iteration}_{k + 1}"
                        ) + '\n'
                else:
                    for k in range(len(device['commands'][i]) - 1):
                        fbd_str += self.output_unit.format(
                            signal=f"{self.dummy_command_output}_{device['name']}_{self.dev_iteration}_{k + 2}"
                        ) + '\n'

                if device['operation'] == 'SBO':
                    # select
                    for k in range(int(len(device['commands'][i]) / 2)):
                        fbd_str += self.output_unit.format(
                            signal=f"{self.dummy_select}_{device['name']}_{self.dev_iteration}_{k + 1}"
                        ) + '\n'

                    # execute
                    for k in range(int(len(device['commands'][i]) / 2)):
                        fbd_str += self.output_unit.format(
                            signal=f"{self.dummy_execute}_{device['name']}_{self.dev_iteration}_{k + 1}"
                        ) + '\n'

            ####################################################################

            # Output header 2
            fbd_str += self.function_block_output_header.format(instance="", size="1") + '\n'

            # output expression
            if device['measurements']:
                fbd_str += self.output_unit.format(signal=device['measurements'][i][0]) + '\n'
            elif device['states']:
                fbd_str += self.output_unit.format(signal=device['states'][i][0]) + '\n'
            elif device['commands']:
                fbd_str += self.output_unit.format(
                    signal=f"{self.dummy_command_output}_{device['name']}_{self.dev_iteration}_1"
                ) + '\n'

            # Update device
            self.dev_iteration += 1

            # Writing the fbd
            file.write(fbd_str)

    def _assign(self, signal, value, file):
        # Inputs
        ####################################################################

        # Input header
        fbd_str = self.assign_input_header + '\n'

        # Input unit
        fbd_str += self.input_unit.format(signal=value) + '\n'

        # Outputs
        ####################################################################

        # Output header 2
        fbd_str += self.function_block_output_header.format(instance="", size="1") + '\n'

        # Output unit
        fbd_str += self.output_unit.format(signal=signal) + '\n'

        # Writing the fbd
        file.write(fbd_str)


class PackLocRemModel(UserPrgModel):
    def __init__(self, user_prg, version):
        if user_prg:
            self.__dict__ = copy.deepcopy(user_prg.__dict__)
        else:
            UserPrgModel.__init__(self, None, None)

        self.pack_loc_rem_model = PackLocRem.objects.filter(Version=version).first()
        self.loc_rem_input = self.pack_loc_rem_model.LocRemInput
        self.loc_rem_input_data_type = self.pack_loc_rem_model.LocRemInputDataType
        self.loc_rem_output = self.pack_loc_rem_model.LocRemOutput
        self.loc_rem_output_data_type = self.pack_loc_rem_model.LocRemOutputDataType
        self.st = self.pack_loc_rem_model.ST

    def pack_loc_rem(self, num_objects, path):
        # Instance data
        pou_name = f"Pack{num_objects}LocalRemote"

        # create file
        pack_object = open(path + "\\" + pou_name + ".EXP", "w+")

        # variable definition
        # Inputs
        input_str = variable_to_declaration(
            signal=self.loc_rem_input,
            size=num_objects,
            data_type=self.loc_rem_input_data_type
        )

        # Outputs
        output_str = f"{self.loc_rem_output} : ARRAY [1..{num_objects}] OF {self.loc_rem_output_data_type};"

        # Declaration construction
        declaration = self.declaration_attributes + '\n'
        declaration += self.declaration_fb_header.format(name=pou_name) + '\n'
        declaration += self.declaration_input.format(input=input_str) + '\n'
        declaration += self.declaration_output.format(output=output_str) + '\n'
        declaration += self.declaration_end_tag + '\n'

        # Code construction
        code = ''
        for i in range(num_objects):
            code += self.st.format(
                output=self.loc_rem_output,
                iterator=(i + 1),
                input=f"{self.loc_rem_input}{i + 1}"
            ) + '\n'
        code += self.code_end_tag

        # Writing the pou
        pack_object.write(declaration + code)

        # closing file
        pack_object.close()

        return pou_name


class CheckLocRemModel(UserPrgModel):
    def __init__(self, user_prg, version):
        if user_prg:
            self.__dict__ = copy.deepcopy(user_prg.__dict__)
        else:
            UserPrgModel.__init__(self, None, None)

        self.check_loc_rem_model = CheckLocRem.objects.filter(Version=version).first()
        self.iterator = self.check_loc_rem_model.Iterator
        self.iterator_data_type = self.check_loc_rem_model.IteratorDataType
        self.st = self.check_loc_rem_model.ST

    def check_loc_rem(self, num_objects, path):
        # Instance data
        pou_name = f"Check{num_objects}LocalRemote"

        # create file
        check_object = open(path + "\\" + pou_name + ".EXP", "w+")

        # variable definition
        # Inputs
        input_str = f"{self.mask_loc_rem} : ARRAY [1..{num_objects}] OF {self.mask_loc_rem_data_type};" + '\n\t'

        # Outputs
        output_str = f"{self.state_loc_rem} : ARRAY [1..{num_objects - 1}] OF {self.state_loc_rem_data_type};" + '\n\t'

        # Internals
        internal_str = f"{self.iterator} : {self.iterator_data_type};" + '\n'

        # Declaration construction
        declaration = self.declaration_attributes + '\n'
        declaration += self.declaration_fb_header.format(name=pou_name) + '\n'
        declaration += self.declaration_input.format(input=input_str) + '\n'
        declaration += self.declaration_output.format(output=output_str) + '\n'
        declaration += self.declaration_internal.format(internal=internal_str) + '\n'
        declaration += self.declaration_end_tag + '\n'

        # Code construction
        code = self.st.format(
            mask_0=self.mask_loc_rem,
            iterator_0=self.iterator,   size_0=num_objects - 1,
            state_0=self.state_loc_rem, iterator_1=self.iterator,
            iterator_2=self.iterator,   size_1=num_objects,
            mask_1=self.mask_loc_rem,   iterator_3=self.iterator,
            state_1=self.state_loc_rem, iterator_4=self.iterator,
            state_2=self.state_loc_rem, iterator_5=self.iterator
        )
        code += '\n' + self.code_end_tag

        # Writing the pou
        check_object.write(declaration + code)

        # Closing file
        check_object.close()

        return pou_name


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
        self.select_data_type = self.device_model.SelectDataType
        self.execute = self.device_model.Execute
        self.execute_data_type = self.device_model.ExecuteDataType

    def device(self, device_name, device_operation, rtu_instance_list, sequence, server_iteration, path):
        # Instance data
        pou_name = "Dev" + str(device_name) + str(server_iteration)

        # create file
        device_object = open(path + "\\" + pou_name + ".EXP", "w+")

        # variable definition
        # inputs
        # control inputs
        input_str = f"{self.first_cycle}        : {self.first_cycle_data_type};" + '\n\t'
        input_str += f"{self.sequence_order}    : {self.sequence_order_data_type};" + '\n\t'
        input_str += f"{self.protocol}          : {self.protocol_data_type};" + '\n\t'
        input_str += f"{self.state_loc_rem}     : {self.state_loc_rem_data_type};" + '\n\t'

        # Obtaining sequence keys to apply individual conditions
        purposes = sequence.keys()

        # measures
        if 'measure' in purposes:
            input_str += variable_to_declaration(
                signal=self.measure,
                size=sequence['measure'],
                data_type=self.measure_data_type
            ) + '\n\t'

            input_str += variable_to_declaration(
                signal=self.save_measure,
                size=sequence['measure'],
                data_type=self.save_measure_data_type
            ) + '\n\t'

            input_str += variable_to_declaration(
                signal=self.name_measure,
                size=sequence['measure'],
                data_type=self.name_measure_data_type
            ) + '\n\t'

        # states
        if 'state' in purposes:
            input_str += variable_to_declaration(
                signal=self.state,
                size=sequence['state'],
                data_type=self.state_data_type
            ) + '\n\t'

            input_str += variable_to_declaration(
                signal=self.save_state,
                size=sequence['state'],
                data_type=self.save_state_data_type
            ) + '\n\t'

            input_str += variable_to_declaration(
                signal=self.name_state,
                size=sequence['state'],
                data_type=self.name_state_data_type
            ) + '\n\t'

            input_str += variable_to_declaration(
                signal=self.rise_state,
                size=sequence['state'],
                data_type=self.rise_state_data_type
            ) + '\n\t'

        # commands
        if 'command' in purposes:
            input_str += variable_to_declaration(
                signal=self.command,
                size=sequence['command'],
                data_type=self.command_data_type
            ) + '\n\t'

            input_str += variable_to_declaration(
                signal=self.save_command,
                size=sequence['command'],
                data_type=self.save_command_data_type
            ) + '\n\t'

            input_str += variable_to_declaration(
                signal=self.name_command,
                size=sequence['command'],
                data_type=self.name_command_data_type
            ) + '\n\t'

            input_str += variable_to_declaration(
                signal=self.trigger_command,
                size=sequence['command'],
                data_type=self.trigger_command_data_type
            ) + '\n\t'

            # inputs sbo
            if device_operation == "SBO":
                input_str += variable_to_declaration(
                    signal=self.status,
                    size=int(sequence['command'] / 2),
                    data_type=self.status_data_type
                ) + '\n\t'

        # Outputs
        output_str = ''
        # measures
        if 'measure' in purposes:
            output_str += variable_to_declaration(
                signal=self.measure_output,
                size=sequence['measure'],
                data_type=self.measure_output_data_type
            ) + '\n\t'

        # states
        if 'state' in purposes:
            output_str += variable_to_declaration(
                signal=self.state_output,
                size=sequence['state'],
                data_type=self.state_output_data_type
            ) + '\n\t'

        # commands
        if 'command' in purposes:
            output_str += variable_to_declaration(
                signal=self.command_output,
                size=sequence['command'],
                data_type=self.command_output_data_type
            ) + '\n\t'

            # outputs sbo
            if device_operation == "SBO":
                output_str += variable_to_declaration(
                    signal=self.select,
                    size=int(sequence['command'] / 2),
                    data_type=self.select_data_type
                ) + '\n\t'

                output_str += variable_to_declaration(
                    signal=self.execute,
                    size=int(sequence['command'] / 2),
                    data_type=self.execute_data_type
                ) + '\n\t'

        # Internals
        internal_str = ''
        for instance in rtu_instance_list:
            internal_str += f"inst0{instance} : {instance};" + '\n\t'

        # Declaration construction
        declaration = self.declaration_attributes + '\n'
        declaration += self.declaration_fb_header.format(name=pou_name) + '\n'
        declaration += self.declaration_input.format(input=input_str) + '\n'
        declaration += self.declaration_output.format(output=output_str) + '\n'
        declaration += self.declaration_internal.format(internal=internal_str) + '\n'
        declaration += self.declaration_end_tag + '\n'
        device_object.write(declaration)

        # Code construction
        device_object.write(self.header.format(size=str(len(purposes))) + '\n')

        # Instantiation
        for i, key in enumerate(purposes):
            self._rtu_fbd(device_operation, rtu_instance_list[i], sequence[key], key, device_object)

        # Final tag
        device_object.write(self.code_end_tag + '\n')

        # Closing file
        device_object.close()

        return pou_name

    def _rtu_fbd(self, device_operation, instance, num_objects, purpose, file):
        # Obtaining data
        rtu_information = self.rtu_decision_tree(purpose)
        input_data = rtu_information['input_data']
        output_data = rtu_information['output_data']
        save_data = rtu_information['save_data']
        name_data = rtu_information['name_data']
        trigger_data = rtu_information['trigger_data']

        # Inputs
        ####################################################################

        # Input size
        num_inputs = 0
        if purpose == 'measure':
            num_inputs = (3 * num_objects) + 5
        elif purpose == 'state':
            num_inputs = (4 * num_objects) + 5
        elif purpose == 'command':
            if device_operation == 'SBO':
                num_inputs = (4 * num_objects) + int(num_objects / 2) + 5
            else:
                num_inputs = (4 * num_objects) + 5

        # Input header
        fbd_str = self.function_block_input_header.format(
            title='',
            instance=f"inst0{instance}",
            size=str(num_inputs)
        ) + '\n'

        # Inputs
        # header
        fbd_str += self.input_unit.format(signal=self.first_cycle) + '\n'
        fbd_str += self.input_unit.format(signal=self.sequence_order) + '\n'
        fbd_str += self.input_unit.format(signal=self.protocol) + '\n'
        fbd_str += self.input_unit.format(signal=self.state_loc_rem) + '\n'
        if purpose == 'command':
            fbd_str += self.input_unit.format(signal="CONTROL") + '\n'
        else:
            fbd_str += self.input_unit.format(signal="MONITOR") + '\n'

        # input data
        for i in range(num_objects):
            fbd_str += self.input_unit.format(signal=f"{input_data}{i + 1}") + '\n'

        # saves
        for i in range(num_objects):
            fbd_str += self.input_unit.format(signal=f"{save_data}{i + 1}") + '\n'

        # names
        for i in range(num_objects):
            fbd_str += self.input_unit.format(signal=f"{name_data}{i + 1}") + '\n'

        # trigger and status
        if purpose != 'measure':
            for i in range(num_objects):
                fbd_str += self.input_unit.format(signal=f"{trigger_data}{i + 1}") + '\n'
            if purpose == 'command' and device_operation == 'SBO':
                for i in range(int(num_objects / 2)):
                    fbd_str += self.input_unit.format(signal=f"{self.status}{i + 1}") + '\n'

        # Outputs
        ####################################################################

        # Output size
        if purpose == 'command' and device_operation == 'SBO':
            num_outputs = (2 * num_objects) - 1
        else:
            num_outputs = num_objects - 1

        # output header 1
        fbd_str += self.function_block_output_header.format(instance=instance, size=num_outputs) + '\n'

        # output unit 1
        for i in range(num_objects - 1):
            fbd_str += self.output_unit.format(signal=f"{output_data}{i + 2}") + '\n'

        if purpose == 'command' and device_operation == 'SBO':
            for i in range(int(num_objects / 2)):
                fbd_str += self.output_unit.format(signal=f"{self.select}{i + 1}") + '\n'
            for i in range(int(num_objects / 2)):
                fbd_str += self.output_unit.format(signal=f"{self.execute}{i + 1}") + '\n'

        # Output header 2
        fbd_str += self.function_block_output_header.format(instance="", size="1") + '\n'

        # output unit 2
        fbd_str += self.output_unit.format(signal=f"{output_data}1") + '\n'

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
        input_str = f"{self.first_cycle}        : {self.first_cycle_data_type};" + '\n\t'
        input_str += f"{self.sequence_order}    : {self.sequence_order_data_type};" + '\n\t'
        input_str += f"{self.protocol}          : {self.protocol_data_type};" + '\n\t'
        input_str += f"{self.state_loc_rem}     : {self.state_loc_rem_data_type};" + '\n\t'
        input_str += f"{self.action}            : {self.action_data_type};" + '\n\t'

        input_str += variable_to_declaration(
            signal=input_data,
            size=num_objects,
            data_type=input_data_type
        ) + '\n\t'

        input_str += variable_to_declaration(
            signal=save_data,
            size=num_objects,
            data_type=save_data_type
        ) + '\n\t'

        input_str += variable_to_declaration(
            signal=name_data,
            size=num_objects,
            data_type=name_data_type
        ) + '\n\t'

        if purpose != 'measure':
            input_str += variable_to_declaration(
                signal=trigger_data,
                size=num_objects,
                data_type=trigger_data_type
            ) + '\n\t'

        if device_operation == "SBO" and purpose == 'command':
            input_str += variable_to_declaration(
                signal=self.status,
                size=int(num_objects / 2),
                data_type=self.status_data_type
            ) + '\n\t'

        # Outputs
        output_str = variable_to_declaration(
            signal=output_data,
            size=num_objects,
            data_type=output_data_type
        ) + '\n\t'

        if device_operation == "SBO" and purpose == 'command':
            output_str += variable_to_declaration(
                signal=self.select,
                size=int(num_objects / 2),
                data_type=self.select_data_type
            ) + '\n\t'

            output_str += variable_to_declaration(
                signal=self.execute,
                size=int(num_objects / 2),
                data_type=self.execute_data_type
            ) + '\n\t'

        # Internals
        internal_str = f"{self.signals}         : ARRAY [1..{num_objects}] OF {input_data_type};" + '\n\t'
        internal_str += f"{self.check_changes}  : ARRAY [1..{num_objects}] OF {self.check_changes_data_type};" + '\n\t'
        internal_str += f"{self.names}          : ARRAY [1..{num_objects}] OF {self.names_data_type};" + '\n\t'
        internal_str += f"{self.saves}          : ARRAY [1..{num_objects}] OF {self.saves_data_type};" + '\n\t'
        internal_str += f"{self.error}          : {self.error_data_type};" + '\n\t'

        if purpose != 'measure':
            internal_str += f"{self.trigger_changes} : ARRAY [1..{num_objects}] OF " \
                            f"{self.trigger_changes_data_type};" + '\n\t'
            if purpose == 'state':
                internal_str += f"{self.rise_changes} : ARRAY [1..{num_objects}] OF " \
                                f"{self.rise_changes_data_type};" + '\n\t'

        for item in instance_list:
            if 'Save' not in item and 'Handler' not in item:    # Save and Handler aren't fb but functions
                internal_str += f"inst0{item} : {item};" + '\n\t'

        # Declaration construction
        declaration = self.declaration_attributes + '\n'
        declaration += self.declaration_fb_header.format(name=pou_name) + '\n'
        declaration += self.declaration_input.format(input=input_str) + '\n'
        declaration += self.declaration_output.format(output=output_str) + '\n'
        declaration += self.declaration_internal.format(internal=internal_str) + '\n'
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
        networks = self.header.format(size=body_networks)
        rtu_object.write(networks + '\n')

        # RTU hub
        if purpose == 'command':
            self._pack_fbd(instance_list[0], num_objects, purpose, 'trigger', rtu_object)
            self._pack_fbd(instance_list[1], num_objects, purpose, 'values', rtu_object)
            self._check_fbd(instance_list[2], rtu_object)
            self._map_fbd(instance_list[3], num_objects, purpose, rtu_object)
            self._pack_fbd(instance_list[4], num_objects, purpose, 'save', rtu_object)
            self._pack_fbd(instance_list[5], num_objects, purpose, 'label', rtu_object)
            self._save_fbd(instance_list[6], purpose, rtu_object)
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
            self._save_fbd(instance_list[7], purpose, rtu_object)
        elif purpose == 'measure':
            self._pack_fbd(instance_list[0], num_objects, purpose, 'values', rtu_object)
            self._check_fbd(instance_list[1], rtu_object)
            self._map_fbd(instance_list[2], num_objects, purpose, rtu_object)
            self._pack_fbd(instance_list[3], num_objects, purpose, 'save', rtu_object)
            self._pack_fbd(instance_list[4], num_objects, purpose, 'label', rtu_object)
            self._save_fbd(instance_list[5], purpose, rtu_object)

        # Final tag
        rtu_object.write(self.code_end_tag + '\n')
        rtu_object.close()

        return pou_name

    def _pack_fbd(self, instance, num_objects, purpose, internal_purpose, file):
        # Obtaining data
        pack_information = self.pack_decision_tree(purpose, internal_purpose)
        input_data = pack_information['input_data']
        output_data = pack_information['output_data']

        # Inputs
        ####################################################################

        # Input header
        fbd_str = self.function_block_input_header.format(
            title='',
            instance=f"inst0{instance}",
            size=str(num_objects)
        ) + '\n'

        # Input unit
        for i in range(num_objects):
            fbd_str += self.input_unit.format(signal=f"{input_data}{i + 1}") + '\n'

        # Outputs
        ####################################################################

        # Output header 1
        fbd_str += self.function_block_output_header.format(instance=instance, size="0") + '\n'

        # Output header 2
        fbd_str += self.function_block_output_header.format(instance="", size="1") + '\n'

        # Output unit
        fbd_str += self.output_unit.format(signal=output_data) + '\n'

        # Writing the fbd
        file.write(fbd_str)

    def _rise_fbd(self, instance, file):
        # Inputs
        ####################################################################

        # Input header
        fbd_str = self.function_block_input_header.format(title='', instance=f"inst0{instance}", size="1") + '\n'

        # Input unit
        fbd_str += self.input_unit.format(signal=self.rise_changes) + '\n'

        # Outputs
        ####################################################################

        # Output header 1
        fbd_str += self.function_block_output_header.format(instance=instance, size="0") + '\n'

        # Output header 2
        fbd_str += self.function_block_output_header.format(instance="", size="1") + '\n'

        # Output unit
        fbd_str += self.output_unit.format(signal=self.trigger_changes) + '\n'

        # Writing the fbd
        file.write(fbd_str)

    def _check_fbd(self, instance, file):
        # Inputs
        ####################################################################

        # Input header
        fbd_str = self.function_block_input_header.format(title='', instance=f"inst0{instance}", size="2") + '\n'

        # Input unit
        fbd_str += self.input_unit.format(signal=self.signals) + '\n'
        fbd_str += self.input_unit.format(signal=self.first_cycle) + '\n'

        # Outputs
        ####################################################################

        # Output header 1
        fbd_str += self.function_block_output_header.format(instance=instance, size="0") + '\n'

        # Output header 2
        fbd_str += self.function_block_output_header.format(instance="", size="1") + '\n'

        # Output unit
        fbd_str += self.output_unit.format(signal=self.check_changes) + '\n'

        # Writing the fbd
        file.write(fbd_str)

    def _map_fbd(self, instance, num_objects, purpose, file):
        # Obtaining data
        map_information = self.map_decision_tree(purpose)
        input_data = map_information['input_data']
        output_data = map_information['output_data']

        # Inputs
        ####################################################################

        # Input size
        if purpose == 'measure':
            inputs = num_objects + 2
        else:
            inputs = (3 * num_objects) + 2

        # Input header
        fbd_str = self.function_block_input_header.format(title='', instance=f"inst0{instance}", size=inputs) + '\n'

        # Input unit
        fbd_str += self.input_unit.format(signal=self.action) + '\n'
        fbd_str += self.input_unit.format(signal=self.state_loc_rem) + '\n'

        # inputs
        for i in range(num_objects):
            fbd_str += self.input_unit.format(signal=f"{input_data}{i + 1}") + '\n'

        if purpose != 'measure':
            # triggers
            for i in range(num_objects):
                fbd_str += self.input_unit.format(signal=f"{self.trigger_changes}[{i + 1}]") + '\n'

            # checks
            for i in range(num_objects):
                fbd_str += self.input_unit.format(signal=f"{self.check_changes}[{i + 1}]") + '\n'

        # Outputs
        ####################################################################

        # Output header 1
        fbd_str += self.function_block_output_header.format(instance=instance, size=str(num_objects - 1)) + '\n'

        # Output unit 1
        for i in range(num_objects - 1):
            fbd_str += self.output_unit.format(signal=f"{output_data}{i + 2}") + '\n'

        # Output header 2
        fbd_str += self.function_block_output_header.format(instance="", size="1") + '\n'

        # Output unit 2
        fbd_str += self.output_unit.format(signal=f"{output_data}1") + '\n'

        # Writing fbd
        file.write(fbd_str)

    def _save_fbd(self, instance, purpose, file):
        # Inputs
        ####################################################################

        # Input header
        fbd_str = self.function_input_header.format(size="9") + '\n'

        # Input unit
        fbd_str += self.input_unit.format(signal=self.first_cycle) + '\n'
        fbd_str += self.input_unit.format(signal=self.sequence_order) + '\n'
        fbd_str += self.input_unit.format(signal=self.protocol) + '\n'
        fbd_str += self.input_unit.format(signal=self.state_loc_rem) + '\n'
        fbd_str += self.input_unit.format(signal=self.action) + '\n'
        fbd_str += self.input_unit.format(signal=self.signals) + '\n'
        fbd_str += self.input_unit.format(signal=self.names) + '\n'
        if purpose == 'measure':
            fbd_str += self.input_unit.format(signal=self.check_changes) + '\n'
        else:
            fbd_str += self.input_unit.format(signal=self.trigger_changes) + '\n'
        fbd_str += self.input_unit.format(signal=self.saves) + '\n'

        # Output header
        fbd_str += self.function_output_header.format(instance=instance) + '\n'

        # Writing the fbd
        file.write(fbd_str)

    def _sbo_fbd(self, instance, num_objects, file):
        # Inputs
        ####################################################################

        # Input header
        fbd_str = self.function_block_input_header.format(
            title='',
            instance=f"inst0{instance}",
            size=str(num_objects + int(num_objects / 2) + 1)
        ) + '\n'

        # Input unit
        fbd_str += self.input_unit.format(signal=self.state_loc_rem) + '\n'

        # Triggers
        for i in range(num_objects):
            fbd_str += self.input_unit.format(signal=f"{self.trigger_changes}[{i + 1}]") + '\n'

        # Status
        for i in range(int(num_objects / 2)):
            fbd_str += self.input_unit.format(signal=f"{self.status}{i + 1}") + '\n'

        # Outputs
        ####################################################################

        # Output header 1
        fbd_str += self.function_block_output_header.format(instance=instance, size=str((num_objects + 1) - 1)) + '\n'

        # Selects
        for i in range(int(num_objects / 2)):
            fbd_str += self.output_unit.format(signal=f"{self.select}{i + 1}") + '\n'

        # Executes
        for i in range(int(num_objects / 2)):
            fbd_str += self.output_unit.format(signal=f"{self.execute}{i + 1}") + '\n'

        # Output header 2
        fbd_str += self.function_block_output_header.format(instance="", size="1") + '\n'

        # Output unit
        fbd_str += self.output_unit.format(signal=self.error) + '\n'

        # Writing the fbd
        file.write(fbd_str)

    def _handler_fbd(self, instance, file):
        # Inputs
        ####################################################################

        # Input header
        fbd_str = self.function_input_header.format(instance=f"inst0{instance}", size="1") + '\n'

        # Input unit
        fbd_str += self.input_unit.format(signal=self.error) + '\n'

        # Function output header
        fbd_str += self.function_output_header.format(instance=instance) + '\n'

        # Writing the fbd
        file.write(fbd_str)

    def pack_decision_tree(self, rtu_purpose, internal_purpose):
        response = {}
        if internal_purpose == 'trigger':
            if rtu_purpose == 'command':
                response['input_data'] = self.trigger_command
                response['output_data'] = self.trigger_changes
                response['input_data_type'] = self.trigger_command_data_type
                response['output_data_type'] = self.trigger_changes_data_type
            elif rtu_purpose == 'state':
                response['input_data'] = self.rise_state
                response['output_data'] = self.rise_changes
                response['input_data_type'] = self.rise_state_data_type
                response['output_data_type'] = self.rise_changes_data_type
        elif internal_purpose == 'label':
            if rtu_purpose == 'command':
                response['input_data'] = self.name_command
                response['input_data_type'] = self.name_command_data_type
            elif rtu_purpose == 'state':
                response['input_data'] = self.name_state
                response['input_data_type'] = self.name_state_data_type
            elif rtu_purpose == 'measure':
                response['input_data'] = self.name_measure
                response['input_data_type'] = self.name_measure_data_type
            response['output_data'] = self.names
            response['output_data_type'] = self.names_data_type
        elif internal_purpose == 'save':
            if rtu_purpose == 'command':
                response['input_data'] = self.save_command
                response['input_data_type'] = self.save_command_data_type
            elif rtu_purpose == 'state':
                response['input_data'] = self.save_state
                response['input_data_type'] = self.save_state_data_type
            elif rtu_purpose == 'measure':
                response['input_data'] = self.save_measure
                response['input_data_type'] = self.save_measure_data_type
            response['output_data'] = self.saves
            response['output_data_type'] = self.saves_data_type
        elif internal_purpose == 'values':
            if rtu_purpose == 'command':
                response['input_data'] = self.command
                response['input_data_type'] = self.command_data_type
                response['output_data_type'] = self.command_data_type
            elif rtu_purpose == 'state':
                response['input_data'] = self.state
                response['input_data_type'] = self.state_data_type
                response['output_data_type'] = self.state_data_type
            elif rtu_purpose == 'measure':
                response['input_data'] = self.measure
                response['input_data_type'] = self.measure_data_type
                response['output_data_type'] = self.measure_data_type
            response['output_data'] = self.signals
        else:
            "gestionar errores"

        return response

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
        response = {
            'input_data': '',
            'input_data_type': '',
            'output_data': '',
            'output_data_type': ''
        }
        if purpose == 'command':
            response['input_data'] = self.command
            response['input_data_type'] = self.command_data_type
            response['output_data'] = self.command_output
            response['output_data_type'] = self.command_output_data_type
        elif purpose == 'state':
            response['input_data'] = self.state
            response['input_data_type'] = self.state_data_type
            response['output_data'] = self.state_output
            response['output_data_type'] = self.state_output_data_type
        elif purpose == 'measure':
            response['input_data'] = self.measure
            response['input_data_type'] = self.measure_data_type
            response['output_data'] = self.measure_output
            response['output_data_type'] = self.measure_output_data_type

        return response

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
        self.st = self.pack_model.ST

    def pack(self, device_name, num_objects, rtu_purpose, internal_purpose, server_iteration, path):
        # Obtaining data
        pack_information = self.pack_decision_tree(rtu_purpose, internal_purpose)
        input_data = pack_information['input_data']
        input_data_type = pack_information['input_data_type']
        output_data = pack_information['output_data']
        output_data_type = pack_information['output_data_type']

        # Instance data
        pou_name = "Pack" + str(num_objects) + input_data_type + internal_purpose + str(
            device_name) + rtu_purpose + str(server_iteration)

        # create file
        pack_object = open(path + "\\" + pou_name + ".EXP", "w+")

        # variable definition
        # Inputs
        input_str = variable_to_declaration(signal=input_data, size=num_objects, data_type=input_data_type)

        # Outputs
        output_str = f"{output_data} : ARRAY [1..{num_objects}] OF {output_data_type};"

        # Declaration construction
        declaration = self.declaration_attributes + '\n'
        declaration += self.declaration_fb_header.format(name=pou_name) + '\n'
        declaration += self.declaration_input.format(input=input_str) + '\n'
        declaration += self.declaration_output.format(output=output_str) + '\n'
        declaration += self.declaration_end_tag + '\n'

        # Code construction
        code = ''
        for i in range(num_objects):
            code += self.st.format(
                output_variable=output_data,
                iterator=(i + 1),
                input_variable=f"{input_data}{i + 1}"
            ) + '\n'
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
        self.st = self.check_model.ST

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
        input_str = f"{input_data}              : ARRAY [1..{num_objects}] OF {input_data_type};" + '\n\t'
        input_str += f"{self.first_cycle}       : {self.first_cycle_data_type};"

        # Outputs
        output_str = f"{output_data}            : ARRAY [1..{num_objects}] OF {output_data_type};"

        # Internals
        internal_str = f"{self.iterator}        : {self.iterator_data_type};" + '\n\t'
        internal_str += f"{self.last_values}    : ARRAY [1..{num_objects}] OF {input_data_type};"

        # Declaration construction
        declaration = self.declaration_attributes + '\n'
        declaration += self.declaration_fb_header.format(name=pou_name) + '\n'
        declaration += self.declaration_input.format(input=input_str) + '\n'
        declaration += self.declaration_output.format(output=output_str) + '\n'
        declaration += self.declaration_internal.format(internal=internal_str) + '\n'
        declaration += self.declaration_end_tag + '\n'

        # Code construction
        code = self.st.format(
            iterator_0=self.iterator,       size=num_objects,
            first_cycle=self.first_cycle,
            last_values_0=self.last_values, iterator_1=self.iterator, values_0=input_data,
            iterator_2=self.iterator,
            values_1=input_data,            iterator_3=self.iterator, last_values_1=self.last_values,
            iterator_4=self.iterator,
            mask_changes_0=output_data,     iterator_5=self.iterator,
            mask_changes_1=output_data,     iterator_6=self.iterator,
            last_values_2=self.last_values, values_2=input_data
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
        self.st = self.map_model.ST

    def map(self, device_name, num_objects, purpose, server_iteration, path):
        # Obtaining data
        map_information = self.map_decision_tree(purpose)
        input_data = map_information['input_data']
        input_data_type = map_information['input_data_type']
        output_data = map_information['output_data']
        output_data_type = map_information['output_data_type']

        # Instance data
        pou_name = "Map" + str(num_objects) + input_data_type + str(device_name) + purpose + str(server_iteration)

        # create file
        map_object = open(path + "\\" + pou_name + ".EXP", "w+")

        # Variable declaration
        # Inputs
        input_str = f"{self.action} : {self.action_data_type};" + '\n\t'
        input_str += f"{self.state_loc_rem} : {self.state_loc_rem_data_type};" + '\n\t'
        input_str += variable_to_declaration(
            signal=input_data,
            size=num_objects,
            data_type=input_data_type
        ) + '\n\t'

        if purpose != 'measure':
            input_str += variable_to_declaration(
                signal=self.trigger_changes,
                size=num_objects,
                data_type=self.trigger_changes_data_type
            ) + '\n\t'
            input_str += variable_to_declaration(
                signal=self.check_changes,
                size=num_objects,
                data_type=self.check_changes_data_type
            )

        # Outputs
        output_str = variable_to_declaration(
            signal=output_data,
            size=num_objects,
            data_type=output_data_type
        )

        # Declaration construction
        declaration = self.declaration_attributes + '\n'
        declaration += self.declaration_fb_header.format(name=pou_name) + '\n'
        declaration += self.declaration_input.format(input=input_str) + '\n'
        declaration += self.declaration_output.format(output=output_str) + '\n'
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
            state_0=self.state_loc_rem,
            state_1=self.state_loc_rem,
            action=self.action,
            mapping=code
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
        self.st = self.rise_model.ST

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
        input_str = f"{input_data}          : ARRAY [1..{num_objects}] OF {input_data_type};"

        # Outputs
        output_str = f"{output_data}        : ARRAY [1..{num_objects}] OF {output_data_type};"

        # Internals
        internal_str = f"{self.last_rise}   : ARRAY [1..{num_objects}] OF {self.last_rise_data_type};" + '\n'
        internal_str += f"{self.iterator}   : {self.iterator_data_type};"

        # Declaration construction
        declaration = ''
        declaration += self.declaration_attributes + '\n'
        declaration += self.declaration_fb_header.format(name=pou_name) + '\n'
        declaration += self.declaration_input.format(input=input_str) + '\n'
        declaration += self.declaration_output.format(output=output_str) + '\n'
        declaration += self.declaration_internal.format(internal=internal_str) + '\n'
        declaration += self.declaration_end_tag + '\n'

        # Code construction
        code = self.st.format(
            iterator_0=self.iterator,   num_objects=num_objects,
            rise_0=input_data,          iterator_1=self.iterator, last_rise_0=self.last_rise, iterator_2=self.iterator,
            trigger_0=output_data,      iterator_3=self.iterator,
            last_rise_1=self.last_rise, iterator_4=self.iterator, rise_1=input_data,          iterator_5=self.iterator,
            trigger_1=output_data,      iterator_6=self.iterator
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
        self.st = self.save_model.ST

    def save(self, device_name, num_objects, purpose, server_iteration, path):
        # Obtaining data
        save_information = self.save_decision_tree(purpose)
        input_data_type = save_information['input_data_type']

        # Instance data
        pou_name = "Save" + str(num_objects) + input_data_type + str(device_name) + purpose + str(server_iteration)

        # create file
        save_object = open(path + "\\" + pou_name + ".EXP", "w+")

        # Variable definition
        # Inputs
        input_str = f"{self.first_cycle}        : {self.first_cycle_data_type};" + '\n'
        input_str += f"{self.sequence_order}    : {self.sequence_order_data_type};" + '\n'
        input_str += f"{self.protocol}          : {self.protocol_data_type};" + '\n'
        input_str += f"{self.state_loc_rem}     : {self.state_loc_rem_data_type};" + '\n'
        input_str += f"{self.action}            : {self.action_data_type};" + '\n'
        input_str += f"{self.signals}           : ARRAY [1..{num_objects}] OF {input_data_type};" + '\n'
        input_str += f"{self.names}             : ARRAY [1..{num_objects}] OF {self.names_data_type};" + '\n'
        input_str += f"{self.check_changes}     : ARRAY [1..{num_objects}] OF {self.check_changes_data_type};" + '\n'
        input_str += f"{self.saves}             : ARRAY [1..{num_objects}] OF {self.saves_data_type};" + '\n'

        # Internals
        internal_str = f"{self.reason}              : {self.reason_data_type} := {self.reason_init_val};" + '\n'
        internal_str += f"{self.time}               : {self.time_data_type};" + '\n'
        internal_str += f"{self.offset}             : {self.offset_data_type};" + '\n'
        internal_str += f"{self.iterator}           : {self.iterator_data_type};" + '\n'
        internal_str += f"{self.power_on_prefix}    : {self.power_on_prefix_data_type} := " \
                        f"{self.power_on_prefix_init_val};" + '\n'
        internal_str += f"{self.prefix_under_line}  : {self.prefix_under_line_data_type} := " \
                        f"{self.prefix_under_line_init_val};" + '\n'
        internal_str += f"{self.delimiter}          : {self.delimiter_data_type} := {self.delimiter_init_val};" + '\n'
        internal_str += f"{self.object_value}       : {self.object_value_data_type};" + '\n'
        internal_str += f"{self.prefix}             : {self.prefix_data_type};" + '\n'
        internal_str += f"{self.file}               : {self.file_data_type};" + '\n'
        internal_str += f"{self.close}              : {self.close_data_type};" + '\n'
        internal_str += f"{self.new_line}           : {self.new_line_data_type} := {self.new_line_init_val};" + '\n'

        # Obtaining hysteresis derivatives
        hysteresis_condition = ""
        internal_input_code = ""
        hysteresis_code_end_tag = ""
        if input_data_type == "WORD":
            hysteresis = Obj35mMeTe.objects.filter(DeviceName=device_name).first().Hysteresis
            if hysteresis:
                internal_str += f"{self.hysteresis} : ARRAY[1..{num_objects}] OF {self.hysteresis_data_type} :=" \
                                f" {hysteresis};" + '\n'
                internal_str += f"{self.last_values} : ARRAY[1..{num_objects}] OF {input_data_type};"
                hysteresis_condition = f"IF ({self.signals}[{self.iterator}] > ({self.last_values}" \
                                       f"[{self.iterator}] + (({self.hysteresis}[{self.iterator}] / 100) * " \
                                       f"{self.last_values}[{self.iterator}] ))) OR ({self.signals}" \
                                       f"[{self.iterator}] < ({self.last_values}[{self.iterator}] - " \
                                       f"(({self.hysteresis}[{self.iterator}] / 100) * {self.last_values}" \
                                       f"[{self.iterator}]))) THEN"
                internal_input_code = f"{self.last_values}[{self.iterator}] := {self.signals}[{self.iterator}];"
                hysteresis_code_end_tag = "END_IF"

        # Declaration construction
        declaration = self.declaration_attributes + '\n'
        declaration += self.declaration_f_header.format(name=pou_name) + '\n'
        declaration += self.declaration_input.format(input=input_str) + '\n'
        declaration += self.declaration_internal.format(internal=internal_str) + '\n'
        declaration += self.declaration_end_tag + '\n'

        # Code construction (every format line represents a line of Structured Text code in the database)
        code = self.st.format(
            file_0=self.file,
            time_0=self.time,
            offset=self.offset, sequence_order_0=self.sequence_order, signals_size_0=num_objects,
            protocol_0=self.protocol, protocol_1=self.protocol, prefix_under_line=self.prefix_under_line,
            prefix_0=self.prefix, protocol_2=self.protocol, sequence_order_data_type=self.sequence_order_data_type,
            sequence_order_1=self.sequence_order,
            first_cycle=self.first_cycle,
            iterator_0=self.iterator, signals_size_1=num_objects,
            saves_0=self.saves, iterator_1=self.iterator,
            save_last_value_0=internal_input_code,
            object_value_0=self.object_value, signal_data_type_0=input_data_type, signal_0=self.signals,
            iterator_2=self.iterator,
            file_1=self.file, time_1=self.time, time_2=self.time,
            file_2=self.file, delimiter_0=self.delimiter, delimiter_1=self.delimiter,
            file_3=self.file, prefix_1=self.prefix, prefix_2=self.prefix,
            file_4=self.file, delimiter_2=self.delimiter, delimiter_3=self.delimiter,
            file_5=self.file, power_on_prefix_0=self.power_on_prefix, power_on_prefix_1=self.power_on_prefix,
            file_6=self.file, names_0=self.names, iterator_3=self.iterator, names_1=self.names,
            iterator_4=self.iterator,
            file_7=self.file, delimiter_4=self.delimiter, delimiter_5=self.delimiter,
            file_8=self.file, object_value_1=self.object_value, object_value_2=self.object_value,
            file_9=self.file, new_line_0=self.new_line, new_line_1=self.new_line,
            iterator_5=self.iterator, signals_size_2=num_objects,
            saves_1=self.saves, iterator_6=self.iterator,
            mask_changes=self.check_changes, iterator_7=self.iterator,
            hysteresis=hysteresis_condition,
            save_last_value_1=internal_input_code,
            object_value_3=self.object_value, signal_data_type_1=input_data_type, signal_1=self.signals,
            iterator_8=self.iterator,
            file_10=self.file, time_3=self.time, time_4=self.time,
            file_11=self.file, delimiter_6=self.delimiter, delimiter_7=self.delimiter,
            file_12=self.file, prefix_3=self.prefix, prefix_4=self.prefix,
            file_13=self.file, delimiter_8=self.delimiter, delimiter_9=self.delimiter,
            file_14=self.file, power_on_prefix_2=self.power_on_prefix, power_on_prefix_3=self.power_on_prefix,
            file_15=self.file, names_2=self.names, iterator_9=self.iterator, names_3=self.names,
            iterator_10=self.iterator,
            file_16=self.file, delimiter_10=self.delimiter, delimiter_11=self.delimiter,
            file_17=self.file, object_value_4=self.object_value, object_value_5=self.object_value,
            file_18=self.file, new_line_2=self.new_line, new_line_3=self.new_line,
            hysteresis_end_tag=hysteresis_code_end_tag,
            close=self.close, file_19=self.file,
            name=pou_name
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
        self.st_body = self.sbo_model.STBody
        self.st_core = self.sbo_model.STCore

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

        input_str += variable_to_declaration(
            signal=self.trigger_changes,
            size=num_objects,
            data_type=self.trigger_changes_data_type
        ) + '\n'

        input_str += variable_to_declaration(
            signal=self.status,
            size=int(num_objects / 2),
            data_type=self.status_data_type
        ) + '\n'

        # Outputs
        output_str = f"{self.error} : {self.error_data_type};" + '\n'

        output_str += variable_to_declaration(
            signal=self.select,
            size=int(num_objects / 2),
            data_type=self.select_data_type
        ) + '\n'

        output_str += variable_to_declaration(
            signal=self.execute,
            size=int(num_objects / 2),
            data_type=self.execute_data_type
        ) + '\n'

        # Internals
        internal_str = f"{self.error_stat_internal} : {self.error_stat_internal_data_type};" + '\n'

        internal_str += variable_to_declaration(
            signal=self.flag,
            size=int(num_objects / 2),
            data_type=self.flag_data_type
        ) + '\n'

        # Declaration construction
        declaration = self.declaration_attributes + '\n'
        declaration += self.declaration_fb_header.format(name=pou_name) + '\n'
        declaration += self.declaration_input.format(input=input_str) + '\n'
        declaration += self.declaration_output.format(output=output_str) + '\n'
        declaration += self.declaration_internal.format(internal=internal_str) + '\n'
        declaration += self.declaration_end_tag + '\n'

        # Code construction
        code_core = ''
        for s in range(int(num_objects / 2)):
            code_core += self.st_core.format(
                flag_0=f"{self.flag}{s + 1}",
                input_n=f"{self.trigger_changes}{(2 * s) + 1}",     input_m=f"{self.trigger_changes}{(2 * s) + 2}",
                select_0=f"{self.select}{s + 1}",
                flag_1=f"{self.flag}{s + 1}",
                flag_2=f"{self.flag}{s + 1}",
                status=f"{self.status}{s + 1}",
                select_1=f"{self.select}{s + 1}",
                select_2=f"{self.select}{s + 1}",
                execute_0=f"{self.execute}{s + 1}",
                execute_1=f"{self.execute}{s + 1}",
                flag_3=f"{self.flag}{s + 1}",
                error_status_internal_0=self.error_stat_internal,
                execute_2=f"{self.execute}{s + 1}",
                select_3=f"{self.select}{s + 1}",
                flag_4=f"{self.flag}{s + 1}",
                error_status_internal_1=self.error_stat_internal,
                execute_3=f"{self.execute}{s + 1}",
                select_4=f"{self.select}{s + 1}",
                flag_5=f"{self.flag}{s + 1}",
                error_status_internal_2=self.error_stat_internal,
            ) + "\n\n"

        code = self.st_body.format(
            error_status_internal_0=self.error_stat_internal,
            state=self.state_loc_rem,
            error_status_output_0=self.error,                    error_status_internal_1=self.error_stat_internal,
            core=code_core,
            error_status_output_1=self.error,                    error_status_internal_2=self.error_stat_internal
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
        self.st = self.handler_model.ST

    def handler(self, device_name, server_iteration, path):
        # Instance data
        pou_name = "Handler" + str(device_name) + str(server_iteration)

        # create file
        handler_object = open(path + "\\" + pou_name + ".EXP", "w+")

        # Variable declaration
        # Inputs
        input_str = f"{self.error} : {self.error_data_type};" + '\n'

        # Internals
        internal_str = f"{self.error_description} : {self.error_description_data_type};" + '\n'

        # Declaration construction
        declaration = self.declaration_attributes + '\n'
        declaration += self.declaration_f_header.format(name=pou_name) + '\n'
        declaration += self.declaration_input.format(input=input_str) + '\n'
        declaration += self.declaration_internal.format(internal=internal_str) + '\n'
        declaration += self.declaration_end_tag + '\n'

        # Code construction
        code = self.st.format(
            input_error_0=self.error,
            input_error_1=self.error,
            description_0=self.error_description,
            description_1=self.error_description,
            description_2=self.error_description,
            description_3=self.error_description,
            description_4=self.error_description,
            pou_name=pou_name
        )
        code += '\n' + self.code_end_tag

        # Writing the pou
        handler_object.write(declaration + code)

        return pou_name
