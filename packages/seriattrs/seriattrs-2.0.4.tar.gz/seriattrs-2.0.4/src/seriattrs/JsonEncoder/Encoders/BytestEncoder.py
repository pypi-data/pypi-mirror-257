from typing import Any

from ...JsonEncoder.Encoder import Encoder


class BytesEncoder(Encoder):
    @staticmethod
    def is_valid(element: Any) -> bool:
        return isinstance(element, bytes)

    @staticmethod
    def encode(element: bytes) -> str:
        return element.decode()
