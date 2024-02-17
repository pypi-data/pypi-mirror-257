from json import JSONEncoder
from typing import Mapping, Sequence

from .Encoder import Encoder


class DefaultJsonEncoder(JSONEncoder):
    @classmethod
    def default(cls, obj, strict: bool=True):
        for encoder in Encoder.__subclasses__():
            if encoder.is_valid(obj):
                return encoder.encode(obj)
        else:
            if strict:
                raise ValueError(obj, "can't be encoded")
            return obj

    @classmethod
    def serialize_values(cls, values, short_term_memory=None):
        if short_term_memory is None:
            short_term_memory = list()
        if values in short_term_memory:
            return values
        else:
            short_term_memory.append(values)
        if isinstance(values, Mapping):
            for key, value in tuple(values.items()):
                values[key] = cls.serialize_values(value, short_term_memory)
            return values
        elif isinstance(values, Sequence):
            for index, item in values:
                values[index] = cls.serialize_values(item, short_term_memory)
            return values
        else:
            return cls._serialize_value(values)

    @classmethod
    def _serialize_value(cls, obj):
        return DefaultJsonEncoder().default(obj, strict=False)
