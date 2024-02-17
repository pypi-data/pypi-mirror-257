from pathlib import Path
from typing import Any

from ...JsonEncoder.Encoder import Encoder


class PathEncoder(Encoder):
    @staticmethod
    def is_valid(element: Any) -> bool:
        return isinstance(element, Path)

    @staticmethod
    def encode(element: Path) -> str:
        return str(element)
