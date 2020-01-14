from project_parts.models import Project as Prj


class Project:
    def __init__(self, date):
        self.date = date
        self.header = Prj.objects.first().Header.format(f"{date:%d/%m/%Y %H:%M:%S}")
        self.closing_tag = Prj.objects.first().ClosingTag

    def headers(self, file):
        file.write(self.header)

    def closing_tags(self, file):
        file.write(self.closing_tag)

