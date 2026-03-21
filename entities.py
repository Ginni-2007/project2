from __future__ import annotations
from typing import Any

class Graph:
    """
    oiergjoiergjeoirgjoeaigjoisj
    """
    _drivers: dict[int, Driver]
    _races: dict[int, Race]

    def __init__(self) -> None:
        """In
        """
        self._drivers = {}
        self._races = {}

    def add_driver(self, id: int, )-> None:
        if id not in self._drivers:
            self._drivers[id] = Driver(the needed parameters)

    def add_race(self, race_id: int, name: str, circuit_id: int) -> None:
        if id not in self._races:
            self._races[race_id] = Race(race_id, name, circuit_id)

    def add_driver_to_race(self, race_id: int, driver_id: int) -> None:

        if race_id not in self._races or driver_id not in self._drivers:
            raise ValueError

        self._races[race_id].add_driver(driver_id, self._drivers[driver_id])


class Race:
    """
    A Race vertex in the graph, used to represent a single race

    Instance Attributes:
        - _race_id: The int id for the race
        - _name: The name of the race
        - _drivers: Dictionary mapping the driver ids to the Driver instances
        - _circuitID: The id of the circuit

    Representation Invariants:
        -
    """
    _race_id: int
    _name: str
    _drivers: dict[int, Driver]
    _circuitID: int

    def __init__(self, race_id: int, name: str, circuit_id: int) -> None:
        """Initialize a new vertex with the given item and kind.

        This vertex is initialized with no neighbours.

        Preconditions:
            - kind in {'user', 'book'}
        """
        self._race_id = race_id
        self._name = name
        self._circuitID = circuit_id

        self._drivers = {}

    def add_driver(self, driver_id: int, driver: Driver) -> None:
        """
        Add the given driver to the drivers dictionary, if driver already present do nothing.
        """
        if driver_id in self._drivers:
            return
        self._drivers[driver_id] = driver

    def connect_drivers(self):




class Driver:
    """
    A single racer
    rigisehbiejgliszm
    """




class RaceData:
    """
    Represent a specific race's data for a racer.

    Instance Attributes:
        - raceID: The id of the race
        - driver_id: The id of the racer
        - starting_position: The position at the start of the race
        - final_position: The position at the end of the race
        - fastest_lap_order: The fastest lap
        - is_sprint: Is this a sprint race or not
        - won_race: Did the racer win the race
        - position_change: The difference in the starting and the final position
        - finish_race: Did the racer finish the race

    Representation Invariants:
        -

    """
    raceID: int
    driver_id: int
    starting_position: int
    final_position: int
    fastest_lap_order: int
    is_sprint: bool
    won_race: bool
    position_change: int
    finish_race: bool

    def __init__(self, race_id: int, driver_id: int, starting_position: int, final_position: int,
                 fastest_lap_order: int, is_sprint: bool, won_race: bool, finish_race: bool) -> None:
        """Initialize a new vertex with the given item and kind.

        This vertex is initialized with no neighbours.

        Preconditions:
            - kind in {'user', 'book'}
        """
        self.raceID = race_id
        self.driver_id = driver_id
        self.starting_position = starting_position
        self.final_position = final_position
        self.fastest_lap_order = fastest_lap_order
        self.is_sprint = is_sprint
        self.won_race = won_race
        self.finish_race = finish_race

        self.position_change = abs(self.starting_position - self.final_position)




