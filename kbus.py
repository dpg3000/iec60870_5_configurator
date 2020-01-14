from cards.models import Card, Kbus as Kb


def clear_class_variable():
    Kbus.kbus_buffer = ""
    Kbus.iterations = 1


def write_kbus(file):
    Kbus.kbus_buffer += Kb.objects.first().FinalTerminal.format(Kbus.iterations)
    Kbus.kbus_buffer += Kb.objects.first().ClosingTag
    file.write(Kbus.kbus_buffer)


class Kbus:
    kbus_buffer = ""
    iterations = 1
    card_list = []
    header_flag = False

    def __init__(self, name):
        self.name = name
        self.headers = Kb.objects.first().Headers
        self.obj_info = Card.objects.filter(Name=name).first().KbusInfo
        if not Kbus.header_flag:
            self._headers()
            Kbus.header_flag = True

    def _headers(self):
        Kbus.kbus_buffer += self.headers + "\n"

    def create_kbus(self, quantity):
        for i in range(quantity):
            xml_object = self.obj_info.format(Kbus.iterations, (i * 16) + 1, (i * 16) + 2, (i * 16) + 3,
                                              (i * 16) + 4, (i * 16) + 5, (i * 16) + 6, (i * 16) + 7, (i * 16) + 8,
                                              (i * 16) + 9, (i * 16) + 10, (i * 16) + 11, (i * 16) + 12, (i * 16) + 13,
                                              (i * 16) + 14, (i * 16) + 15, (i * 16) + 16)

            Kbus.kbus_buffer += xml_object + "\n"
            Kbus.iterations += 1
