from server_parts.models import Server as Serv, ObjsInfo, Obj35mMeTe, Obj31mDpTb, Obj30mSpTb, Obj58cScTa, Obj59cDcTa
from devs.models import Device
from cards.models import Card
from support_functions import ioa_to_address, update_address
import pou


class Server:
    def __init__(self, name, server_iteration):
        self.name = name
        self.server_iteration = server_iteration
        self.header = Serv.objects.first().Header
        self.closing_tag = Serv.objects.first().ClosingTag

    def headers(self, file):
        header = self.header.format(self.name, str(self.server_iteration), str(2404 + self.server_iteration),
                                    str(self.server_iteration))
        file.write(header)

    def closing_tags(self, file):
        file.write(self.closing_tag)


class ServerDevice:
    def __init__(self, name, element, server_iteration):
        self.name = name
        self.element = element
        self.server_iteration = server_iteration
        self.monitor_ioa = Device.objects.filter(Name=name).first().MonitorIoa
        self.monitor_ioa_jump = Device.objects.filter(Name=name).first().MonitorIoaJump
        self.monitor_obj_list = str(Device.objects.filter(Name=name).first().MonitorObjectList).split(",")
        self.monitor_obj_list = [i.strip() for i in self.monitor_obj_list]
        self.control_ioa = Device.objects.filter(Name=name).first().ControlIoa
        self.control_ioa_jump = Device.objects.filter(Name=name).first().ControlIoaJump
        self.control_obj_list = str(Device.objects.filter(Name=name).first().ControlObjectList).split(",")
        self.control_obj_list = [i.strip() for i in self.control_obj_list]
        self.internal_monitor_ioa = self.monitor_ioa
        self.internal_control_ioa = self.control_ioa
        self.device_count = -1

    def create_device(self, quantity, file):
        for iteration in range(quantity):
            self._update_monitor_ioa()
            self._update_control_ioa()
            self.device_count += 1
            print(self.monitor_obj_list)
            if self.monitor_obj_list:
                for monitor_object in self.monitor_obj_list:
                    if monitor_object == 'obj_35m_me_te':
                        try:
                            obj_info = ObjsInfo.objects.filter(ObjCode=monitor_object).first().ObjInfo
                            sva = Obj35mMeTe.objects.filter(DeviceName=self.name).first().SVA.split(",")
                            if not Obj35mMeTe.objects.filter(DeviceName=self.name).first().Hysteresis:
                                hysteresis = ["1"] * len(sva)
                            else:
                                hysteresis = Obj35mMeTe.objects.filter(DeviceName=self.name).first().Hysteresis.split(",")
                            self._obj_35m_me_te(obj_info, hysteresis, sva, file)
                        except:
                            return f"There is no {monitor_object} for the device {self.name}. You have to add it in the " \
                                   f"server_parts section in the DB "
                    elif monitor_object == 'obj_31m_dp_tb':
                        try:
                            obj_info = ObjsInfo.objects.filter(ObjCode=monitor_object).first().ObjInfo
                            dpi = Obj31mDpTb.objects.filter(DeviceName=self.name).first().DPI.split(",")
                            self._obj_31m_dp_tb(obj_info, dpi, file)
                        except:
                            return f"There is no {monitor_object} for the device {self.name}. You have to add it in the " \
                                   f"server_parts section in the DB "
                    elif monitor_object == 'obj_30m_sp_tb':
                        try:
                            obj_info = ObjsInfo.objects.filter(ObjCode=monitor_object).first().ObjInfo
                            spi = Obj30mSpTb.objects.filter(DeviceName=self.name).first().SPI.split(",")
                            self._obj_30m_sp_tb(obj_info, spi, file)
                        except:
                            return f"There is no {monitor_object} for the device {self.name}. You have to add it in the " \
                                   f"server_parts section in the DB "
                    else:
                        return f"There is no logic to process the {monitor_object}"
            elif self.control_obj_list:
                print("ENTRO EN CONTROL")
                for control_object in self.control_obj_list:
                    if control_object == 'obj_58c_sc_ta':
                        try:
                            obj_info = ObjsInfo.objects.filter(ObjCode=control_object).first().ObjInfo
                            scs = Obj58cScTa.objects.filter(DeviceName=self.name).first().SCS.split(",")
                            self._obj_58c_sc_ta(obj_info, scs, file)
                        except:
                            return f"There is no {control_object} for the device {self.name}. You have to add it to the " \
                                   f"server_parts section in the DB "
                    elif control_object == 'obj_59c_dc_ta':
                        try:
                            obj_info = ObjsInfo.objects.filter(ObjCode=control_object).first().ObjInfo
                            dcs = Obj59cDcTa.objects.filter(DeviceName=self.name).first().DCS.split(",")
                            self._obj_59c_dc_ta(obj_info, dcs, file)
                        except:
                            return f"There is no {control_object} for the device {self.name}. You have to add it to the " \
                                   f"server_parts section in the DB "
                    else:
                        return f"There is no logic to process the {control_object}"
            else:
                "gestionar errores"

    def _obj_35m_me_te(self, obj_info, hysteresis, sva, file):
        address = ioa_to_address(self.internal_monitor_ioa)
        object_measures = []
        object_names = []
        for i in range(len(sva)):
            measure_id = sva[i].format(self.server_iteration, self.device_count).strip()
            measure_id_split = measure_id.split("_")
            name = measure_id_split[2]

            xml_obj = obj_info.format(
                text_first_octet=address[0],
                text_second_octet=address[1],
                text_third_octet=address[2],
                ioa=self.internal_monitor_ioa,
                comment=measure_id,
                third_octet=address[2],
                second_octet=address[1],
                first_octet=address[0],
                hysteresis=hysteresis[i],
                signal=measure_id
            )

            self.internal_monitor_ioa += 1
            address = update_address(address)
            file.write(xml_obj)
            object_measures.append(measure_id)
            object_names.append(name)
        pou.measurements_list.append(object_measures)
        pou.measurements_names_list.append(object_names)

    def _obj_31m_dp_tb(self, obj_info, dpi, file):
        address = ioa_to_address(self.internal_monitor_ioa)
        object_states = []
        object_names = []
        for i in range(len(dpi)):
            state_id_0 = dpi[i].format(self.server_iteration, 0, self.device_count).strip()
            state_id_1 = dpi[i].format(self.server_iteration, 1, self.device_count).strip()
            state_id_0_split = state_id_0.split("_")
            state_id_1_split = state_id_1.split("_")
            name_0 = f"{state_id_0_split[2]}_{state_id_0_split[3]}"
            name_1 = f"{state_id_1_split[2]}_{state_id_1_split[3]}"

            xml_obj = obj_info.format(
                text_first_octet=address[0],
                text_second_octet=address[1],
                text_third_octet=address[2],
                ioa=self.internal_monitor_ioa,
                comment=f"{state_id_0} / {state_id_1}",
                third_octet=address[2],
                second_octet=address[1],
                first_octet=address[0],
                signal_0=state_id_0,
                signal_1=state_id_1
            )

            self.internal_monitor_ioa += 1
            address = update_address(address)
            file.write(xml_obj)
            object_states.append(state_id_0)
            object_states.append(state_id_1)
            object_names.append(name_0)
            object_names.append(name_1)

        pou.states_list.append(object_states)
        pou.states_names_list.append(object_names)

    def _obj_30m_sp_tb(self, obj_info, spi, file):
        address = ioa_to_address(self.internal_monitor_ioa)
        object_states = []
        object_names = []
        for i in range(len(spi)):
            state_id = ''
            if self.element == 'card':
                state_id = spi[i].format(self.server_iteration, (16 * self.device_count) + (i + 1)).strip()
            elif self.element == 'device':
                state_id = spi[i].format(self.server_iteration, self.device_count).strip()
            else:
                "gestionar errores"
            state_id_split = state_id.split("_")
            name = state_id_split[2]

            xml_obj = obj_info.format(
                text_first_octet=address[0],
                text_second_octet=address[1],
                text_third_octet=address[2],
                ioa=self.internal_monitor_ioa,
                comment=state_id,
                third_octet=address[2],
                second_octet=address[1],
                first_octet=address[0],
                signal=state_id
            )

            self.internal_monitor_ioa += 1
            address = update_address(address)
            file.write(xml_obj)
            object_states.append(state_id)
            object_names.append(name)

        pou.states_list.append(object_states)
        pou.states_names_list.append(object_names)

    def _obj_58c_sc_ta(self, obj_info, scs, file):
        address = ioa_to_address(self.internal_control_ioa)
        object_commands = []
        object_names = []
        object_triggers = []
        for i in range(len(scs)):
            command_id = ''
            name = ''
            trigger = ''
            if self.element == 'device':
                command_id = scs[i].format(self.server_iteration, self.device_count).strip()
                command_id_split = command_id.split("_")
                name = command_id_split[2]
                trigger = f"{command_id_split[0]}_{command_id_split[1]}_{command_id_split[2]}_Trigger_" \
                          f"{command_id_split[3]}_{command_id_split[4]}"
            elif self.element == 'card':
                command_id = scs[i].format(self.server_iteration, (16 * self.device_count) + (i + 1)).strip()
                command_id_split = command_id.split("_")
                name = command_id_split[2]
                trigger = f"{command_id}_Trigger"
            else:
                "gestionar errores"

            xml_obj = obj_info.format(
                text_first_octet=address[0],
                text_second_octet=address[1],
                text_third_octet=address[2],
                ioa=self.internal_control_ioa,
                comment=command_id,
                third_octet=address[2],
                second_octet=address[1],
                first_octet=address[0],
                signal=command_id,
                new_value=trigger
            )

            self.internal_control_ioa += 1
            address = update_address(address)
            file.write(xml_obj)
            object_commands.append(command_id)
            object_names.append(name)
            object_triggers.append(trigger)

        pou.commands_list.append(object_commands)
        pou.commands_names_list.append(object_names)
        pou.commands_triggers_list.append(object_triggers)

    def _obj_59c_dc_ta(self, obj_info, dcs, file):
        address = ioa_to_address(self.internal_control_ioa)
        object_commands = []
        object_names = []
        object_triggers = []
        for i in range(len(dcs)):
            command_0_id = dcs[i].format(self.server_iteration, 0, self.device_count).strip()
            command_1_id = dcs[i].format(self.server_iteration, 1, self.device_count).strip()
            command_0_id_split = command_0_id.split("_")
            command_1_id_split = command_1_id.split("_")
            name_0 = f"{command_0_id_split[2]}_{command_0_id_split[3]}"
            name_1 = f"{command_1_id_split[2]}_{command_1_id_split[3]}"
            trigger = f"{command_0_id_split[0]}_{command_0_id_split[1]}_{command_0_id_split[2]}_Trigger_" \
                      f"{command_0_id_split[4]}_{command_0_id_split[5]} "

            xml_obj = obj_info.format(
                text_first_octet=address[0],
                text_second_octet=address[1],
                text_third_octet=address[2],
                ioa=self.internal_control_ioa,
                comment=f"{command_0_id} / {command_1_id}",
                third_octet=address[2],
                second_octet=address[1],
                first_octet=address[0],
                signal_0=command_0_id,
                signal_1=command_1_id,
                new_value=trigger
            )

            self.internal_control_ioa += 1
            address = update_address(address)
            file.write(xml_obj)
            object_commands.append(command_0_id)
            object_commands.append(command_1_id)
            object_names.append(name_0)
            object_names.append(name_1)
            object_triggers.append(trigger)
            object_triggers.append(trigger)

        pou.commands_list.append(object_commands)
        pou.commands_names_list.append(object_names)
        pou.commands_triggers_list.append(object_triggers)

    def _update_monitor_ioa(self):
        if self.internal_monitor_ioa != self.monitor_ioa:
            self.internal_monitor_ioa = self.monitor_ioa + (self.device_count + 1) * self.monitor_ioa_jump

    def _update_control_ioa(self):
        if self.internal_control_ioa != self.control_ioa:
            self.internal_control_ioa = self.control_ioa + (self.device_count + 1) * self.control_ioa_jump


class ServerCard:
    def __init__(self, name, server_iteration):
        self.name = name
        self.server_iteration = server_iteration
        self.monitor_ioa = Card.objects.filter(Name=name).first().MonitorIoa
        self.monitor_ioa_jump = Card.objects.filter(Name=name).first().MonitorIoaJump
        self.monitor_obj_list = Card.objects.filter(Name=name).first().MonitorObjectList.split(",")
        self.monitor_obj_list = [i.strip() for i in self.monitor_obj_list]
        self.control_ioa = Card.objects.filter(Name=name).first().ControlIoa
        self.control_ioa_jump = Card.objects.filter(Name=name).first().ControlIoaJump
        self.control_obj_list = Card.objects.filter(Name=name).first().ControlObjectList.split(",")
        self.control_obj_list = [i.strip() for i in self.control_obj_list]
        self.internal_monitor_ioa = self.monitor_ioa
        self.internal_control_ioa = self.control_ioa
        self.card_count = -1

    def create_card(self, quantity, file):
        for iteration in range(quantity):
            self._update_monitor_ioa()
            self._update_control_ioa()
            self.card_count += 1
            for monitor_object in self.monitor_obj_list:
                if monitor_object == 'obj_30m_sp_tb':
                    obj_info = ObjsInfo.objects.filter(ObjCode=monitor_object).first().ObjInfo
                    spi = Obj30mSpTb.objects.filter(DeviceName=self.name).first().SPI.split(",")
                    self._obj_30m_sp_tb(obj_info, spi, file)
            for control_object in self.control_obj_list:
                if control_object == 'obj_58c_sc_ta':
                    obj_info = ObjsInfo.objects.filter(ObjCode=control_object).first().ObjInfo
                    scs = Obj58cScTa.objects.filter(DeviceName=self.name).first().SCS.split(",")
                    self._obj_58c_sc_ta(obj_info, scs, file)

    def _obj_30m_sp_tb(self, obj_info, spi, file):
        address = ioa_to_address(self.internal_monitor_ioa)
        object_states = []
        object_names = []
        for i in range(len(spi)):
            state_id = spi[i].format(self.server_iteration, (16 * self.card_count) + (i + 1)).strip()
            state_id_split = state_id.split("_")
            name = state_id_split[2]

            xml_obj = obj_info.format(
                text_first_octet=address[0],
                text_second_octet=address[1],
                text_third_octet=address[2],
                ioa=self.internal_monitor_ioa,
                comment=state_id,
                third_octet=address[2],
                second_octet=address[1],
                first_octet=address[0],
                signal=state_id
            )

            self.internal_monitor_ioa += 1
            address = update_address(address)
            file.write(xml_obj)
            object_states.append(state_id)
            object_names.append(name)

        pou.states_list.append(object_states)
        pou.states_names_list.append(object_names)

    def _obj_58c_sc_ta(self, obj_info, scs, file):
        address = ioa_to_address(self.internal_control_ioa)
        object_commands = []
        object_names = []
        object_triggers = []
        for i in range(len(scs)):
            command_id = scs[i].format(self.server_iteration, (16 * self.card_count) + (i + 1)).strip()
            command_id_split = command_id.split("_")
            name = command_id_split[2]
            trigger = f"{command_id}_Trigger"

            xml_obj = obj_info.format(
                text_first_octet=address[0],
                text_second_octet=address[1],
                text_third_octet=address[2],
                ioa=self.internal_control_ioa,
                comment=command_id,
                third_octet=address[2],
                second_octet=address[1],
                first_octet=address[0],
                signal=command_id,
                new_value=trigger
            )

            self.internal_control_ioa += 1
            address = update_address(address)
            file.write(xml_obj)
            object_commands.append(command_id)
            object_names.append(name)
            object_triggers.append(trigger)

        pou.commands_list.append(object_commands)
        pou.commands_names_list.append(object_names)
        pou.commands_triggers_list.append(object_triggers)

    def _update_monitor_ioa(self):
        if self.internal_monitor_ioa != self.monitor_ioa:
            self.internal_monitor_ioa = self.monitor_ioa + (self.card_count + 1) * self.monitor_ioa_jump

    def _update_control_ioa(self):
        if self.internal_control_ioa != self.control_ioa:
            self.internal_control_ioa = self.control_ioa + (self.card_count + 1) * self.control_ioa_jump
