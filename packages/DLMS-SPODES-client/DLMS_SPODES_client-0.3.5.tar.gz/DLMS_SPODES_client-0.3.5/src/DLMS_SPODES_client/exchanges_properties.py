from typing import TypeAlias
from dataclasses import dataclass


class InitType:
    """nothing params"""


@dataclass
class ReadAttribute:
    ln: str
    index: int


ExProp: TypeAlias = InitType | ReadAttribute
