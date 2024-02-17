import re
import typing
from abc import ABCMeta
from collections import defaultdict
from inspect import signature
from types import GenericAlias
from typing import Any, get_args, ForwardRef

from attr import fields

_ = typing


class DbClassCreator(ABCMeta):
    """Metaclass that converts Forward references to class instances.

    @define
    class Bar(DbClass):
        foo: "Foo" => Foo

    @define
    class Foo(DbClass):
        bar: "Bar" => Bar
    """
    _type_checked_fields = defaultdict(list)
    _created_types = {}

    def __new__(cls, name: str, bases: tuple, namespace: dict[str, Any]):
        new_class = super().__new__(cls, name, bases, namespace)
        for field_name, field_type in new_class.__annotations__.items():
            forward_refs = cls._get_forward_refs(field_type)
            for forward_ref in forward_refs:
                if forward_ref in cls._created_types:
                    new_class.__annotations__[field_name] = cls._update_hint(forward_ref,
                                                                             new_class.__annotations__[field_name])
                else:
                    cls._type_checked_fields[forward_ref].append(new_class)
        cls._created_types[ForwardRef(name)] = new_class
        for db_class in cls._type_checked_fields.get(ForwardRef(name), []):
            attrs_fields = []
            for f in fields(db_class):
                forward_refs = cls._get_forward_refs(f.type)
                current_string_type = f.type
                for forward_ref in forward_refs:
                    if forward_ref not in cls._created_types:
                        continue
                    current_string_type = cls._update_hint(forward_ref, current_string_type)
                field_value = dict((arg, getattr(f, arg)) for arg in signature(type(f)).parameters if hasattr(f, arg))
                field_value['type'] = current_string_type
                field_value['cmp'] = None
                new_field = type(f)(**field_value)
                attrs_fields.append(new_field)
            db_class.__attrs_attrs__ = type(db_class.__attrs_attrs__)(attrs_fields)
        return new_class

    @classmethod
    def _get_forward_refs(cls, field_type):
        forward_refs = list(ForwardRef(ref) if isinstance(ref, str) else ref for ref in get_args(field_type) if
                            isinstance(ref, (str, ForwardRef)))
        if isinstance(field_type, str):
            forward_refs.append(ForwardRef(field_type))
        return forward_refs

    @classmethod
    def _update_hint(cls, forward_ref: ForwardRef, current_string_type: GenericAlias) -> GenericAlias:
        forward_ref_name = cls._created_types[forward_ref].__name__
        return eval(
            re.sub(r'(?:ForwardRef\(|)\'' + forward_ref_name + r'\'\)?', forward_ref_name, str(current_string_type)),
            globals(), {forward_ref_name: cls._created_types[forward_ref]}
        )
