

# hiuwhttuh4
# rhfiwaheglgrehiwh
class Graph:
    """
    still need to add the first one
    """

    _drivers: list[Driver]
    _races: list[Race]

    def find_driver_by_id(self):
        """
        return racer by given racer id
        """

    def add_races(self):
        """
        adds a race to the _races
        """
    def add_race_data(self):
        """
        add race data from results.csv
        """

class Race:
    """
    A single Race
    """
    _drivers: list[Driver]
    _name: str
    _circuitID: int
    _year: int

    def add_driver(self, ):
        """

        """
    def connect_drivers(self):
        """
        connects all the drivers in a given race
        """
        for driver in self._drivers:
            for driver2 in self._drivers:
                if driver2 in driver._racer_to_raceID:
                    driver._racer_to_race[driver2].union(self)
                else:
                    driver._racer_to_race[driver2] = set(self)

class Driver:
    """
    A single racer
    """
    _name: str
    _raced_before_with: list[Driver]
    _racer_to_raceID: dict[Driver, set[int]] # {diver name: the raceID they were together}
    _races: list[RaceData]

    def add_race(self):
        """
        adds the race to the list of races in a driver
        """

class RaceData:
    """
    contains a SINGLE racer's data for a single race based on raceID
    """
    raceID: str
    grid: int
    position: int
    fastest_lap_order: int
    is_sprint: bool
