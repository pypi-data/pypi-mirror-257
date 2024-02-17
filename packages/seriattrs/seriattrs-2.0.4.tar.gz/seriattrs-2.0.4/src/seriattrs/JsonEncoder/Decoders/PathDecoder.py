from pathlib import Path
from typing import Any

from ...JsonEncoder import Decoder


class PathDecoder(Decoder):
    @staticmethod
    def is_valid(element: Any) -> bool:
        return isinstance(element, str)

    @staticmethod
    def decode(element: str, _) -> Path:
        return Path(element)
