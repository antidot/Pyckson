class Serializer:
    def serialize(self, obj):
        pass


class BasicSerializer(Serializer):
    def serialize(self, obj):
        return obj


class ListSerializer(Serializer):
    def __init__(self, sub_serializer: Serializer):
        self.sub_serializer = sub_serializer

    def serialize(self, obj):
        return [self.sub_serializer.serialize(item) for item in obj]


class EnumSerializer(Serializer):
    def serialize(self, obj):
        return obj.name


class BasicDictSerializer(Serializer):
    def serialize(self, obj):
        return obj


class TypingDictSerializer(Serializer):
    def __init__(self, value_serializer: Serializer):
        self.value_serializer = value_serializer

    def serialize(self, obj):
        return {k: self.value_serializer.serialize(v) for k, v in obj.items()}
