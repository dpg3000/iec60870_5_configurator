from django.db import models
import copy

# Pou versions menu
user_prg_version = 'userprgv0'
device_version = 'devicev0'
rtu_version = 'rtuv0'

# Data object repository for pou interface management
fbd_model = None
fb_model = None
user_prg_model = None
device_model = None
rtu_model = None
pack_model = None
map_model = None
rise_model = None
check_model = None
save_model = None


# Create your models here.
class Rtu(models.Model):
    Version = models.CharField(max_length=255)
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

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(Rtu, self).save()
        models.rtu_model = RtuModel(device_model, fbd_model, rtu_version)

    def __str__(self):
        return self.Version


class Map(models.Model):
    Version = models.CharField(max_length=255)
    ST = models.TextField(default="")

    def __str__(self):
        return self.Version


class Check(models.Model):
    Version = models.CharField(max_length=255)
    Iterator = models.CharField(max_length=255, default="")
    IteratorDataType = models.CharField(max_length=255, default="")
    LastValues = models.CharField(max_length=255, default="")
    LastValuesDataType = models.CharField(max_length=255, default="")
    ST = models.TextField()

    def __str__(self):
        return self.Version


class Save(models.Model):
    Version = models.CharField(max_length=255)
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

    def __str__(self):
        return self.Version


class FBDTemplate(models.Model):
    Header = models.TextField(default="")
    InputHeader = models.TextField(default="")
    InputUnit = models.TextField(default="")
    OutputHeader = models.TextField(default="")
    OutputUnit = models.TextField(default="")


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
    TriggerState = models.CharField(max_length=255, default="")
    TriggerStateDataType = models.CharField(max_length=255, default="")
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
        models.device_model = DeviceModel(fbd_model, user_prg_model, device_version)

    def __str__(self):
        return self.Version


class RiseToTrigger(models.Model):
    Version = models.CharField(max_length=255)
    LastRise = models.CharField(max_length=255, default="")
    LastRiseDataType = models.CharField(max_length=255, default="")
    Iterator = models.CharField(max_length=255, default="")
    IteratorDataType = models.CharField(max_length=255, default="")
    ST = models.TextField(default="")

    def __str__(self):
        return self.Version


class UserPrg(models.Model):
    Version = models.CharField(max_length=255)
    FirstCycle = models.CharField(max_length=255, default="")
    FirstCycleDataType = models.CharField(max_length=255, default="")
    MaskLocRem = models.CharField(max_length=255, default="")
    MaskLocRemDataType = models.CharField(max_length=255, default="")
    LocRemState = models.CharField(max_length=255, default="")
    LocRemStateDataType = models.CharField(max_length=255, default="")

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(UserPrg, self).save()
        models.user_prg_model = UserPrgModel(fbd_model, user_prg_version)

    def __str__(self):
        return self.Version


class FBTemplate(models.Model):
    DeclarationAttributes = models.TextField(default="")
    DeclarationFBHeader = models.CharField(max_length=255, default="")
    DeclarationFHeader = models.CharField(max_length=255, default="")
    DeclarationInput = models.TextField(default="")
    DeclarationOutput = models.TextField(default="")
    DeclarationInternal = models.TextField(default="")
    DeclarationEndTag = models.CharField(max_length=255, default="")
    CodeEndTag = models.CharField(max_length=255, default="")


class FunctionBlockDiagramModel:
    def __init__(self):
        self.function_block_diagram_template = FBDTemplate.objects.first()
        self.header = self.function_block_diagram_template.Header
        self.input_header = self.function_block_diagram_template.InputHeader
        self.input_unit = self.function_block_diagram_template.InputUnit
        self.output_header = self.function_block_diagram_template.OutputHeader
        self.output_unit = self.function_block_diagram_template.OutputUnit


class FunctionBlockModel:
    def __init__(self):
        self.function_block_template = FBTemplate.objects.first()
        self.declaration_attribute = self.function_block_template.DeclarationAttributes
        self.declaration_fb_header = self.function_block_template.DeclarationFBHeader
        self.declaration_f_header = self.function_block_template.DeclarationFHeader
        self.declaration_input = self.function_block_template.DeclarationInput
        self.declaration_output = self.function_block_template.DeclarationOutput
        self.declaration_internal = self.function_block_template.DeclarationInternal
        self.declaration_end_tag = self.function_block_template.DeclarationEndTag
        self.code_end_tag = self.function_block_template.CodeEndTag


class UserPrgModel(FunctionBlockDiagramModel):
    # Copy constructor implementation
    def __init__(self, fbd, version):
        if fbd:
            self.__dict__ = copy.deepcopy(fbd.__dict__)
        else:
            FunctionBlockDiagramModel.__init__(self)

        self.user_prg_model = UserPrg.objects(Version=version).first()
        self.first_cycle = user_prg_model.FirstCycle
        self.first_cycle_data_type = user_prg_model.FirstCycleDataType
        self.mask_loc_rem = user_prg_model.MaskLocRem
        self.mask_loc_rem_data_type = user_prg_model.MaskLocRemDataType
        self.loc_rem_state = user_prg_model.LocRemState
        self.loc_rem_state_data_type = user_prg_model.LocRemStateDataType


class DeviceModel(FunctionBlockDiagramModel, UserPrgModel):
    # Copy constructor implementation
    def __init__(self, fbd, user_prg, version):
        if fbd:
            self.__dict__ = copy.deepcopy(fbd.__dict__)
        else:
            FunctionBlockDiagramModel.__init__(self)

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
        self.trigger_state = self.device_model.TriggerState
        self.trigger_state_data_type = self.device_model.TriggerStateDataType
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


class RtuModel(DeviceModel, FunctionBlockDiagramModel):
    # Copy constructor implementation
    def __init__(self, device, fbd, version):
        if device:
            self.__dict__ = copy.deepcopy(device.__dict__)
        else:
            DeviceModel.__init__(self, None, None, None)

        if fbd:
            self.__dict__ = copy.deepcopy(fbd.__dict__)
        else:
            FunctionBlockDiagramModel.__init__(self)

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
        self.names = self.rtu_model.NamesDataType
        self.names_data_type = self.rtu_model.NamesDataType
        self.saves = self.rtu_model.Saves
        self.saves_data_type = self.rtu_model.SavesDataType
