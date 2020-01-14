from devs.models import Device
from clients.models import Client as Cl
from support_functions import asdu_to_ioa, update_address, update_address_2


def clear_class_variables():
    Client.client_103_iteration = 1
    Client.protocol_list = []
    Client.asdu_address_104 = [0, 0, 1]
    Client.ip_address_104 = [192, 168, 181, 100]
    Client.buffer_103 = ""
    Client.buffer_104 = ""


def write_client(file):
    buffer = ""
    if Client.buffer_103:
        buffer += Client.buffer_103 + "\n" + "</CClient103>" + "\n"
    if Client.buffer_104:
        buffer += Client.buffer_104 + "\n" + "</CClient104>" + "\n"
    file.write(buffer)


class Client:
    client_103_iteration = 1
    protocol_list = []
    asdu_address_104 = [0, 0, 1]
    ip_address_104 = [192, 168, 181, 100]
    buffer_103 = ""
    buffer_104 = ""

    def __init__(self, name):
        self.name = name
        self.protocol = Device.objects.filter(Name=name).first().Protocol
        self.objs_info = Device.objects.filter(Name=name).first().ClientObjs
        self.client_signals = Device.objects.filter(Name=name).first().ClientSignals.split(",")
        self.client_headers = Cl.objects.filter(Protocol=self.protocol).first().Headers
        self.connection_headers = Cl.objects.filter(Protocol=self.protocol).first().ConnectionHeaders
        self.closing_tag = Cl.objects.filter(Protocol=self.protocol).first().ClosingTag
        if self.protocol not in Client.protocol_list:
            self._headers()
            Client.protocol_list.append(self.protocol)

    def _headers(self):
        if self.protocol == "103":
            Client.buffer_103 += self.client_headers + "\n"
        if self.protocol == "104":
            Client.buffer_104 += self.client_headers + "\n"

    def create_client(self, quantity):
        if self.protocol == "103":
            for i in range(quantity):
                xml_connection = self.connection_headers.format(str(Client.client_103_iteration).zfill(3),
                                                                str(Client.client_103_iteration).zfill(3),
                                                                Client.client_103_iteration,
                                                                Client.client_103_iteration,
                                                                Client.client_103_iteration - 1,
                                                                Client.client_103_iteration - 1,
                                                                Client.client_103_iteration - 1)

                Client.buffer_103 += xml_connection + "\n"
                objs_info = self.objs_info
                for s in range(len(self.client_signals)):
                    index = objs_info.find("{}")
                    string_temp = objs_info[:index] + \
                                  self.client_signals[s].format(Client.client_103_iteration - 1).strip() + \
                                  objs_info[index + 2:]
                    objs_info = string_temp

                Client.buffer_103 += objs_info + "\n"
                Client.client_103_iteration += 1

        if self.protocol == "104":
            for i in range(quantity):
                xml_connection = self.connection_headers.format(str(Client.asdu_address_104[1]).zfill(3),
                                                                str(Client.asdu_address_104[2]).zfill(3),
                                                                asdu_to_ioa(Client.asdu_address_104),
                                                                Client.ip_address_104[0], Client.ip_address_104[1],
                                                                Client.ip_address_104[2], Client.ip_address_104[3],
                                                                Client.asdu_address_104[1], Client.asdu_address_104[2])

                Client.buffer_104 += xml_connection + "\n"
                Client.buffer_104 += self.objs_info + "\n"
                Client.asdu_address_104 = update_address(Client.asdu_address_104)
                Client.ip_address_104 = update_address_2(Client.ip_address_104)
