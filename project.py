from project_parts.models import Project as Prj


class Project:
    def __init__(self, date, file):
        self.date = date
        self.file = file
        self.header = Prj.objects.first().Header.format(f"{date:%d/%m/%Y %H:%M:%S}")
        self.closing_tag = Prj.objects.first().ClosingTag

    def headers(self):
        self.file.write(self.header)

    def closing_tags(self):
        self.file.write(self.closing_tag)

