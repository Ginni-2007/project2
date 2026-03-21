from __future__ import annotations
from typing import Any


class Graph:
    """
    A graph representing relationships between drivers and races.

    This graph stores Driver and Race objects and models interactions between
    drivers based on the races they have both participated in.

    Instance Attributes:
        - _drivers: A dictionary mapping driver IDs to Driver objects
        - _races: A dictionary mapping race IDs to Race objects

    Representation Invariants:
        - All keys in _drivers are unique driver IDs
        - All keys in _races are unique race IDs
    """
    _drivers: dict[int, Driver]
    _races: dict[int, Race]

    def __init__(self) -> None:
        """
        Initialize an empty Graph with no drivers or races
        """
        self._drivers = {}
        self._races = {}

    def add_driver(self, id: int, name: str) -> None:
        """
        Add a new driver to the graph.

        Preconditions:
            - id >= 0
        """
        if id not in self._drivers:
            self._drivers[id] = Driver(id, name)

    def add_race(self, race_id: int, name: str, circuit_id: int) -> None:
        """
        Add a new race to the graph.

        Preconditions:
            - race_id >= 0
        """
        if id not in self._races:
            self._races[race_id] = Race(race_id, name, circuit_id)

    def add_driver_to_race(self, race_id: int, driver_id: int, driver_race_data: list) -> None:
        """
        Add a driver to a specific race.
        Raises ValueError if the race or driver does not exist.

        Preconditions:
           - race_id is in self._races
           - driver_id is in self._drivers
        """
        if race_id not in self._races or driver_id not in self._drivers:
            raise ValueError

        self._races[race_id].add_driver(driver_id, self._drivers[driver_id], driver_race_data)

    def add_edge(self):
        """
        Create edges between drivers who have competed in the same race.
        For each race, connect every pair of drivers as opponents and record the race ID in their shared history.
        """
        for race in self._races.values():
            for d1, d2 in race.get_all_driver_pairs():
                d1.add_opponent(d2, race.get_id())
                d2.add_opponent(d1, race.get_id())

    def get_shared_races(self, d1: Driver, d2: Driver) -> set[int]:
        """Return the set of race IDs where both drivers competed together.

            Preconditions:
                - d1 and d2 are drivers in this graph
            """
        return d1.get_races_against(d2)


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
        """
        Initialize a Race with no drivers.

        Preconditions:
            - race_id >= 0
        """
        self._race_id = race_id
        self._name = name
        self._circuitID = circuit_id

        self._drivers = {}

    def get_id(self) -> int:
        """Return the ID of this race."""
        return self._race_id

    def num_drivers(self) -> int:
        """Return number of drivers that raced"""
        return len(self._drivers)

    def add_driver(self, driver_id: int, driver: Driver, driver_race_data: list) -> None:
        """
        Add the given driver to the drivers dictionary, if driver already present do nothing.
        driver_race_data is a list [startingposition, final position, fastest lap order, issprint, wonrace, positionchange, finish race]
        """
        if driver_id in self._drivers:
            return
        self._drivers[driver_id] = driver
        driver.add_race_data(self._race_id, driver_id, driver_race_data)

    def get_drivers(self) -> list[Driver]:
        """Return a list of all drivers participating in this race."""
        lst = []
        for driver in self._drivers:
            lst += self._drivers[driver]
        return lst

    def get_all_driver_pairs(self) -> list[tuple[Driver, Driver]]:
        """
        Return all ordered pairs of distinct drivers in this race.
        Each pair represents two drivers who competed in the same race.
        """
        id_tuple = (sorted(a, b) for a in self._drivers for b in self._drivers if a != b)
        final_tuple = [(self._drivers[x[0]], self._drivers[x[1]]) for x in id_tuple]
        return final_tuple


class Driver:
    """
    A Driver object representing a single racer.

    Instance Attributes:
        - driver_id: The unique ID of the driver
        - name: The name of the driver
        - neighbours: A set of drivers this driver has competed against
        - racer_to_races: A mapping from a driver to the set of race IDs
                          where they competed against this driver

    Representation Invariants:
        - driver_id >= 0
        - For every driver in neighbours, there is a corresponding key in racer_to_races
    """
    driver_id: int
    name: str
    neighbours: set[Driver]
    racer_to_races: dict[Driver, set[int]]
    past_races: dict[int, RaceData]

    def __init__(self, driver_id: int, name: str) -> None:
        """
        Initialize a driver to driver_id, name, neighbour to empty set and racer_to_races to empty dictionary.
        """
        self.driver_id = driver_id
        self.name = name
        self.neighbours = set()
        self.racer_to_races = {}

    def add_opponent(self, other_driver: Driver, race_id: int):
        """
        Record that this driver competed against another driver in a race.
        If the opponent is new, add them to neighbours and initialize tracking.
        """
        if other_driver not in self.neighbours:
            self.neighbours.add(other_driver)
            self.racer_to_races[other_driver] = set()
        self.racer_to_races[other_driver].add(race_id)

    def get_races_against(self, other_driver: Driver) -> set[int]:
        """
        Return the set of race IDs where this driver competed against other_driver.
        Preconditions:
            - other_driver is in self.neighbours
        """
        return self.racer_to_races[other_driver]

    def add_race_data(self, driver_race_data: list) -> None:
        race_data = RaceData(race_id=driver_race_data[0], driver_id=driver_race_data[1],
                             starting_position=driver_race_data[2], final_position=driver_race_data[3],
                             fastest_lap_order=driver_race_data[4], is_sprint=driver_race_data[5],
                             won_race=driver_race_data[6], position_change=driver_race_data[7],
                             finish_race=driver_race_data[8])
        self.past_races[driver_race_data[0]] = race_data


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
