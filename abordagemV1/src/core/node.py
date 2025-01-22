from __future__ import annotations
from typing import Tuple

class Node():
    parent: Node | None
    position: Tuple[int, int]

    def __init__(self, parent: Node, position: Tuple[int, int]):
        self.parent = parent
        self.position = position

    def __eq__(self, other: Node):
        return self.position == other.position
