import random
from typing import Any, Self

from attr import define, fields, field

from .DbClassCreator import DbClassCreator
from ..JsonEncoder import Decoder, DefaultJsonEncoder
from .._db_attrs_converter import _db_attrs_converter


@define
class DbClass(metaclass=DbClassCreator):
    """Database Class that implements serialize and deserialize methods.
    Each object of a class is provided with int64 number as an id.
    Whenever field contains a DbClass instance _id field on DbClass is used instead. If an actual class is to be used use DbClassLiteral as a base.
    DbClass is an abstract class and must be extended in order to create new instances.

    :var _id: int64 value provided by default to each instance of a DbClass. Can't be initialized but can be changed after initialization.
    """
    _id = field(init=False, type=Any, factory=lambda: random.randint(-2 ** 63, 2 ** 63 - 1))

    def __attrs_post_init__(self):
        if hasattr(self, 'id'):
            self._id = self.id
        self._decode()

    def serialize(self) -> dict:
        from .DbClassLiteral import DbClassLiteral

        return DefaultJsonEncoder.serialize_values(
            dict(
                (
                    f.name,
                    getattr(self, f.name)._id
                    if isinstance(getattr(self, f.name), DbClass)
                       and not isinstance(getattr(self, f.name), DbClassLiteral)
                    else getattr(self, f.name),
                )
                for f in fields(type(self))
            ),
        )

    @classmethod
    def deserialize(cls, dictionary: dict) -> Self:
        type(cls).temp_instances = {}
        deserialized = _db_attrs_converter.structure(dictionary, cls)
        type(cls).temp_instances = {}
        return deserialized

    def _decode(self):
        for f in fields(type(self)):
            for decoder in Decoder.__subclasses__():
                if decoder.is_valid(f.type):
                    setattr(self, f.name, decoder.decode(getattr(self, f.name), f.type))
                    break
