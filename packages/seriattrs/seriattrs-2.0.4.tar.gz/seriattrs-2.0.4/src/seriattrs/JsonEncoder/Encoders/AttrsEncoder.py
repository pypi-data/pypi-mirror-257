import json
from typing import Any, Mapping, Sequence

from attr import has
from attr._make import fields

from ..DefaultJsonEncoder import DefaultJsonEncoder
from ...JsonEncoder import Encoder


class AttrsEncoder(Encoder):
    @staticmethod
    def is_valid(element: Any) -> bool:
        return has(element)

    @staticmethod
    def encode(element) -> dict:
        from ..DefaultJsonEncoder import DefaultJsonEncoder
        from ... import DbClassLiteral, DbClass

        if isinstance(element, DbClassLiteral) or not isinstance(element, DbClass):
            memory = {}
            dictionary = asdict(element, memory=memory)
            fill_memory_gaps(memory, memory)
            return DefaultJsonEncoder.serialize_values(dictionary)
        return element._id


def fill_memory_gaps(memory_item, memory, short_term_memory = None):
    if short_term_memory is None:
        short_term_memory = list()
    if memory_item in short_term_memory:
        return
    else:
        short_term_memory.append(memory_item)
    if isinstance(memory_item, Mapping):
        for key, value in tuple(memory_item.items()):
            if isinstance(value, _Id):
                memory_item[key] = memory[memory_item[key]]
            else:
                fill_memory_gaps(value, memory, short_term_memory)
    elif isinstance(memory_item, Sequence):
        for index, item in memory_item:
            if isinstance(item, _Id):
                memory_item[index] = memory[item]
            else:
                fill_memory_gaps(item, memory, short_term_memory)
    elif isinstance(memory_item, _Id):
        raise ValueError

class _Id(int):
    pass



def asdict(
    inst,
    recurse=True,
    filter=None,
    dict_factory=dict,
    retain_collection_types=False,
    value_serializer=None,
    memory=None,
):
    """
    Return the *attrs* attribute values of *inst* as a dict.

    Optionally recurse into other *attrs*-decorated classes.

    :param inst: Instance of an *attrs*-decorated class.
    :param bool recurse: Recurse into classes that are also
        *attrs*-decorated.
    :param callable filter: A callable whose return code determines whether an
        attribute or element is included (``True``) or dropped (``False``).  Is
        called with the `attrs.Attribute` as the first argument and the
        value as the second argument.
    :param callable dict_factory: A callable to produce dictionaries from.  For
        example, to produce ordered dictionaries instead of normal Python
        dictionaries, pass in ``collections.OrderedDict``.
    :param bool retain_collection_types: Do not convert to ``list`` when
        encountering an attribute whose type is ``tuple`` or ``set``.  Only
        meaningful if ``recurse`` is ``True``.
    :param Optional[callable] value_serializer: A hook that is called for every
        attribute or dict key/value.  It receives the current instance, field
        and value and must return the (updated) value.  The hook is run *after*
        the optional *filter* has been applied.

    :rtype: return type of *dict_factory*

    :raise attrs.exceptions.NotAnAttrsClassError: If *cls* is not an *attrs*
        class.

    ..  versionadded:: 16.0.0 *dict_factory*
    ..  versionadded:: 16.1.0 *retain_collection_types*
    ..  versionadded:: 20.3.0 *value_serializer*
    ..  versionadded:: 21.3.0 If a dict has a collection for a key, it is
        serialized as a tuple.
    """
    if memory is None:
        memory = {}
    if id(inst) not in memory:
        memory[id(inst)] = None
    elif memory[id(inst)] is None:
        memory[id(inst)] = _Id(id(inst))
        return memory[id(inst)]
    else:
        return memory[id(inst)]
    attrs = fields(inst.__class__)
    rv = dict_factory()
    for a in attrs:
        v = getattr(inst, a.name)
        if filter is not None and not filter(a, v):
            continue

        if value_serializer is not None:
            v = value_serializer(inst, a, v)

        if recurse is True:
            if has(v.__class__):
                rv[a.name] = asdict(
                    v,
                    recurse=True,
                    filter=filter,
                    dict_factory=dict_factory,
                    retain_collection_types=retain_collection_types,
                    value_serializer=value_serializer,
                    memory=memory,
                )
            elif isinstance(v, (tuple, list, set, frozenset)):
                cf = v.__class__ if retain_collection_types is True else list
                rv[a.name] = cf(
                    [
                        _asdict_anything(
                            i,
                            is_key=False,
                            filter=filter,
                            dict_factory=dict_factory,
                            retain_collection_types=retain_collection_types,
                            value_serializer=value_serializer,
                            memory=memory,
                        )
                        for i in v
                    ]
                )
            elif isinstance(v, dict):
                df = dict_factory
                rv[a.name] = df(
                    (
                        _asdict_anything(
                            kk,
                            is_key=True,
                            filter=filter,
                            dict_factory=df,
                            retain_collection_types=retain_collection_types,
                            value_serializer=value_serializer,
                            memory=memory,
                        ),
                        _asdict_anything(
                            vv,
                            is_key=False,
                            filter=filter,
                            dict_factory=df,
                            retain_collection_types=retain_collection_types,
                            value_serializer=value_serializer,
                            memory=memory,
                        ),
                    )
                    for kk, vv in v.items()
                )
            else:
                rv[a.name] = v
        else:
            rv[a.name] = v
    memory[id(inst)] = rv
    return rv


def _asdict_anything(
    val,
    is_key,
    filter,
    dict_factory,
    retain_collection_types,
    value_serializer,
    memory,
):
    """
    ``asdict`` only works on attrs instances, this works on anything.
    """
    if id(val) in memory:
        return memory[id(val)]
    if getattr(val.__class__, "__attrs_attrs__", None) is not None:
        # Attrs class.
        rv = asdict(
            val,
            recurse=True,
            filter=filter,
            dict_factory=dict_factory,
            retain_collection_types=retain_collection_types,
            value_serializer=value_serializer,
            memory=memory,
        )
    elif isinstance(val, (tuple, list, set, frozenset)):
        if retain_collection_types is True:
            cf = val.__class__
        elif is_key:
            cf = tuple
        else:
            cf = list

        rv = cf(
            [
                _asdict_anything(
                    i,
                    is_key=False,
                    filter=filter,
                    dict_factory=dict_factory,
                    retain_collection_types=retain_collection_types,
                    value_serializer=value_serializer,
                    memory=memory,
                )
                for i in val
            ]
        )
    elif isinstance(val, dict):
        df = dict_factory
        rv = df(
            (
                _asdict_anything(
                    kk,
                    is_key=True,
                    filter=filter,
                    dict_factory=df,
                    retain_collection_types=retain_collection_types,
                    value_serializer=value_serializer,
                    memory=memory,
                ),
                _asdict_anything(
                    vv,
                    is_key=False,
                    filter=filter,
                    dict_factory=df,
                    retain_collection_types=retain_collection_types,
                    value_serializer=value_serializer,
                    memory=memory,
                ),
            )
            for kk, vv in val.items()
        )
    else:
        rv = val
        if value_serializer is not None:
            rv = value_serializer(None, None, rv)
    memory[id(val)] = rv
    return rv
