from __future__ import annotations
from typing import Any

class Graph:
    """

    """




class Race:
    """
    A Race vertex in the graph, used to represent a single race

    Instance Attributes:
        - item:
        - kind: The type of this vertex: 'user' or 'book'.
        - neighbours: The vertices that are adjacent to this vertex.

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
        - self.kind in {'user', 'book'}
    """
    _race_id: int
    _name: str
    _drivers: dict[int, Driver]
    _circuitID: int
    _year: int

    def __init__(self, item: Any, kind: str) -> None:
        """Initialize a new vertex with the given item and kind.

        This vertex is initialized with no neighbours.

        Preconditions:
            - kind in {'user', 'book'}
        """
        self.item = item
        self.kind = kind
        self.neighbours = set()

class Driver:
    """
    A single racer
    """



class RaceData:
    """
    contains a SINGLE racer's data for a single race based on raceID
    """
