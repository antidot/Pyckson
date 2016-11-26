class EnumParser:
    def parse(self, value):
        pass


class DefaultEnumParser:
    def __init__(self, cls):
        self.cls = cls

    def parse(self, value):
        return self.cls[value]


class CaseInsensitiveParser:
    def __init__(self, cls):
        self.cls = cls
        self.values = {member.name.lower(): member for member in cls}

    def parse(self, value):
        return self.values[value.lower()]
