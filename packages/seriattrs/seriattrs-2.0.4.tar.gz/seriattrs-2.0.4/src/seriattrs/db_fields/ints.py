from functools import partial

from attr import field, validators


def _check_int(instance, attribute, value, bits: int):
    if value < -(2 ** (bits - 1)):
        raise ValueError(f"{value=} must be more than {-(2 ** (bits - 1))}")
    if value > 2 ** (bits - 1) - 1:
        raise ValueError(f"{value=} must be less than {2 ** (bits - 1) - 1}")


def _check_uint(instance, attribute, value, bits: int):
    if value < 0:
        raise ValueError(f"{value=} must be positive")
    if value > 2**bits - 1:
        raise ValueError(f"{value=} must be less than {2 ** bits - 1}")

#: Field which can be used to store int8 values
int8 = partial(
    field, validator=[validators.instance_of(int), partial(_check_int, bits=8)]
)
#: Field which can be used to store int16 values
int16 = partial(
    field, validator=[validators.instance_of(int), partial(_check_int, bits=16)]
)
#: Field which can be used to store int32 values
int32 = partial(
    field, validator=[validators.instance_of(int), partial(_check_int, bits=32)]
)
#: Field which can be used to store int64 values
int64 = partial(
    field, validator=[validators.instance_of(int), partial(_check_int, bits=64)]
)
#: Field which can be used to store uint8 values
uint8 = partial(
    field, validator=[validators.instance_of(int), partial(_check_uint, bits=8)]
)
#: Field which can be used to store uint16 values
uint16 = partial(
    field, validator=[validators.instance_of(int), partial(_check_uint, bits=16)]
)
#: Field which can be used to store uint32 values
uint32 = partial(
    field, validator=[validators.instance_of(int), partial(_check_uint, bits=32)]
)
#: Field which can be used to store uint64 values
uint64 = partial(
    field, validator=[validators.instance_of(int), partial(_check_uint, bits=64)]
)
