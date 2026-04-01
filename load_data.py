"""
CSC111 Project 2: F1 Driver Comparison - Data Loading Module
====================================================================================================

This module contains functions to load Formula 1 data from CSV files and construct
a graph-based representation of drivers and races. It processes driver details,
race data, and race results to use for head-to-head performance analysis.

Copyright and Usage Information
===============================================================================================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for this project, please reach out to the group!

This file is Copyright (c) 2026 Huda Anum, Grishma Arun Kumar, Mehal Patel, Jolly Yan
"""

import csv
from entities import Graph


def load_f1_data(drivers_csv: str, races_csv: str, results_csv: str, sprint_result_csv: str) -> Graph:
    """Return a Graph with the drivers, races and results loaded in from the CSV files.
    The Graph will contain all drivers and races, with edges created between the drivers who have competed in the same
    race.

    Preconditions:
        - drivers_csv is a CSV file containing F1 driver data
        - races_csv is a CSV file containing F1 race data
        - results_csv is a CSV file containing F1 results data

    """
    f1_graph = Graph()

    # call helper methods to load in files
    _load_drivers(f1_graph, drivers_csv)

    _load_races(f1_graph, races_csv)

    _load_results(f1_graph, results_csv)
    _load_results(f1_graph, sprint_result_csv)

    # create edges between drivers who raced together
    f1_graph.add_edge()
    return f1_graph


def _load_drivers(f1_graph: Graph, filename: str) -> None:
    """Helper method to load drivers from CSV file into the graph.
    """
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)

        driver_id_index = header.index("driverId")
        forename_index = header.index("forename")
        surname_index = header.index("surname")
        code_name = header.index('code')

        for row in reader:
            driver_id = int(row[driver_id_index])
            full_name = row[forename_index] + " " + row[surname_index]
            f1_graph.add_driver(driver_id, full_name, row[code_name])


def _load_races(f1_graph: Graph, filename: str) -> None:
    """Helper method to load races from CSV file into the graph.
    """
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)

        race_id_index = header.index("raceId")
        name_index = header.index("name")
        circuit_index = header.index("circuitId")

        for row in reader:
            race_id = int(row[race_id_index])
            name = row[name_index]
            circuit_id = int(row[circuit_index])
            f1_graph.add_race(race_id, name, circuit_id)


def _load_results(f1_graph: Graph, filename: str) -> None:
    """Helper method to load rseults from CSV file and link drivers to races.
    """
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)

        race_id_index = header.index("raceId")
        driver_id_index = header.index("driverId")

        for row in reader:
            race_id = int(row[race_id_index])
            driver_id = int(row[driver_id_index])

            # Citation: Chatgpt
            row_dict = dict(zip(header, row))
            driver_race_data = []
            if filename == 'Dataset/results.csv':
                driver_race_data = _get_driver_race_data(row_dict)
            if filename == 'Dataset/sprint_results.csv':
                driver_race_data = _get_driver_sprint_race_data(row_dict)

            if f1_graph.has_driver(driver_id) and f1_graph.has_race(race_id):
                f1_graph.add_driver_to_race(race_id, driver_id, driver_race_data)


def _get_driver_race_data(row: dict) -> list:
    """Helper function to process a single row from results_csv and return the data that entities.py requires.
    The returned list contains: [start_position, final_position, fastest_lap, is_sprint, won_race, finish_race]

    >>> # doctest 1: driver who finished the race and won
    >>> row1 = {"grid": "1", "positionOrderUse": "1", "position": "1", "fastestLapOrder": "1"}
    >>> _get_driver_race_data(row1)
    [1, 1, 1, False, True, True]

    >>> # doctest 2: driver who did not finish the race
    >>> row2 = {"grid": "10", "positionOrderUse": "18", "position": "\\\\N", "fastestLapOrder": "15"}
    >>> _get_driver_race_data(row2)
    [10, 18, 15, False, False, False]
    """
    start_position = int(row["grid"])
    final_position = int(row["positionOrderUse"])
    fastest_lap = int(row["fastestLapOrder"])
    won_race = False
    finish_race = True

    if row["position"] == "\\N":
        finish_race = False

    if final_position == 1:
        won_race = True

    return [start_position, final_position, fastest_lap, False, won_race, finish_race]


def _get_driver_sprint_race_data(row: dict) -> list:
    """Helper function to process a single row from results_csv and return the data that entities.py requires.
    The returned list contains: [start_position, final_position, fastest_lap, is_sprint, won_race, finish_race]
    >>> # doctest 1: driver who finished the race and won
    >>> row1 = {"grid": "1", "positionOrderUse": "1", "position": "1", "lapPoints": "1"}
    >>> _get_driver_sprint_race_data(row1)
    [1, 1, 1, True, True, True]

    >>> # doctest 2: driver who did not finish the race
    >>> row2 = {"grid": "10", "positionOrderUse": "18", "position": "\\\\N", "lapPoints": "0"}
    >>> _get_driver_sprint_race_data(row2)
    [10, 18, 0, True, False, False]

    """
    start_position = int(row["grid"])
    final_position = int(row["positionOrderUse"])
    fastest_lap = int(row["lapPoints"])
    won_race = False
    finish_race = True

    if row["position"] == "\\N":
        finish_race = False

    if final_position == 1:
        won_race = True

    return [start_position, final_position, fastest_lap, True, won_race, finish_race]


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    import python_ta

    python_ta.check_all(config={
        "extra-imports": ["csv", "entities"],
        "allowed-io": ["load_f1_data",
                       "_load_drivers",
                       "_load_races",
                       "_load_results"
                       ],
        "max-line-length": 120
    })
