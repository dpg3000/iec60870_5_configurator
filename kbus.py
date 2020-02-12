from cards.models import Card, Kbus


class BusModule:
    def __init__(self, article_no):
        self.card_model = Card.objects.filter(ArticleNo=article_no).first()
        self.article_no = article_no
        self.sub_bus_name = self.card_model.SubBusName
        self.io = self.card_model.IO
        self.type = self.card_model.ModuleType
        self.channels = self.card_model.ModuleChannels

        # kbus module info
        self.kbus_model = Kbus.objects.first()
        self.terminal = self.kbus_model.Terminal

        if self.io == 'DI':
            self.signal = self.kbus_model.DISignal
            self.private_channel = self.kbus_model.PrivateInputChannel
            self.public_channel = self.kbus_model.PublicInputChannel
        elif self.io == 'DO':
            self.signal = self.kbus_model.DOSignal
            self.private_channel = self.kbus_model.PrivateOutputChannel
            self.public_channel = self.kbus_model.PublicOutputChannel


def assemble_modules(modules_list, file):
    module_str = ''
    last_index = 0
    di_counter = 0
    do_counter = 0
    counter = 0
    for index, module in enumerate(modules_list):
        # evaluate di/do
        if module.io == 'DI':
            di_counter += 1
            counter = di_counter
        elif module.io == 'DO':
            do_counter += 1
            counter = do_counter

        # private channels
        private_str = ''
        for i in range(int(module.channels)):
            private_str += module.private_channel.format(
                index_0=((counter - 1) * int(module.channels) + (i + 1)),
                index_1=((counter - 1) * int(module.channels) + (i + 1))
            ) + '\n'

        # public channels
        public_str = ''
        for i in range(int(module.channels)):
            public_str += module.public_channel.format(
                index_0=((counter - 1) * int(module.channels) + (i + 1)),
                signal=f"{module.signal}{(counter - 1) * int(module.channels) + (i + 1)}",
                index_1=((counter - 1) * int(module.channels) + (i + 1))
            ) + '\n'

        channel_str = f"{private_str}\n{public_str}"

        # configuring module
        module_str += module.terminal.format(
            sub_bus_id=index + 1,
            sub_bus_name=module.sub_bus_name,
            article_no=module.article_no,
            module_type=module.type,
            module_channels=module.channels,
            channels=channel_str
        ) + '\n'

        last_index = index + 1

    # whole kbus string
    kbus_body = Kbus.objects.first().Body
    bus_str = kbus_body.format(modules=module_str, index=last_index + 1)

    # Writing the object
    file.write(bus_str)
