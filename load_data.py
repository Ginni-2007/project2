"""
TODO
"""

import csv
from entities import Graph


def load_f1_data(drivers_csv: str, races_csv: str, results_csv: str) -> Graph:
    """Return a Graph with the drivers, races and results loaded in from the CSV files.
    The Graph will contain all drivers and races, with edges created between the drivers who have competed in the same
    race.

    Preconditions:
        - drivers_csv is a CSV file containing F1 driver data
        - races_csv is a CSV file containing F1 race data
        - results_csv is a CSV file containing F1 results data
    """
    f1_graph = Graph()

    # load the drivers first
    # with open(drivers_csv, "r", encoding="utf-8") as f:
    #     reader = csv.DictReader(f)
    #     for row in reader:
    #         driver_id = int(row["driverId"])
    #         full_name = row['forename'] + " " + row['surname']
    #         f1_graph.add_driver(driver_id, full_name)

    with open(drivers_csv, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)

        driver_id_index = header.index("driverId")
        forename_index = header.index("forename")
        surname_index = header.index("surname")

        for row in reader:
            driver_id = int(row[driver_id_index])
            full_name = row[forename_index] + " " + row[surname_index]
            f1_graph.add_driver(driver_id, full_name)

    # load the races
    # with open(races_csv, "r", encoding="utf-8") as f:
    #     reader = csv.DictReader(f)
    #     for row in reader:
    #         race_id = int(row["raceId"])
    #         name = row["name"]
    #         circuit_id = int(row["circuitId"])
    #         f1_graph.add_race(race_id, name, circuit_id)

    with open(races_csv, "r", encoding="utf-8") as f:
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

    # load the results
    # with open(results_csv, "r", encoding="utf-8") as f:
    #     reader = csv.DictReader(f)
    #     for row in reader:
    #         race_id = int(row["raceId"])
    #         driver_id = int(row["driverId"])
    #
    #         driver_race_data = _get_driver_race_data(row)
    #
    #         # add the data to the graph by checking if the driver and race exist in our graph
    #         if f1_graph.has_driver(driver_id) and f1_graph.has_race(race_id):
    #             f1_graph.add_driver_to_race(race_id, driver_id, driver_race_data)

    with open(results_csv, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)

        race_id_index = header.index("raceId")
        driver_id_index = header.index("driverId")

        for row in reader:
            race_id = int(row[race_id_index])
            driver_id = int(row[driver_id_index])

            row_dict = dict(zip(header, row))
            driver_race_data = _get_driver_race_data(row_dict)

            if f1_graph.has_driver(driver_id) and f1_graph.has_race(race_id):
                f1_graph.add_driver_to_race(race_id, driver_id, driver_race_data)

    # create edges between drivers who raced together
    f1_graph.add_edge()
    return f1_graph


def _get_driver_race_data(row: dict) -> list:
    """Helper function to process a single row from results_csv and return the data that entities.py requires
    """
    start_position = int(row["grid"])

    # determine what the driver's final position was and finish status
    if row["position"] != "\\N" and row["position"] != " ":
        final_position = int(row["position"])
        finish_race = True
    else:
        final_position = 50
        finish_race = False

    # determine the fastest lap rank
    if row["fastestLapOrder"] != "\\N" and row["fastestLapOrder"] != " ":
        fastest_lap = int(row["fastestLapOrder"])
    else:
        fastest_lap = 99

    # determine if they won
    if final_position == 1:
        won_race = True
    else:
        won_race = False

    return [start_position, final_position, fastest_lap, False, won_race, finish_race]


if __name__ == "__main__":
    import python_ta
    python_ta.check_all(config={
        "extra-imports": ["csv", "entities"],
        "allowed-io": ["load_f1_data"],
        "max-line-length": 120
    })
