"""
CSC111 Project 2:- Beyond the Podium: A battle between F1’s greatest
========================================================

This module serves as the main entry point for the F1 driver head-to-head
analysis. It provides an interactive command-line interface that allows
users to explore driver networks, compare performance metrics between drivers,
and generate visualizations of both the driver relationship network and
head-to-head statistics. The system integrates data loading, network analysis,
and interactive visualizations.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for this project, please reach out to the group!

This file is Copyright (c) 2026 Huda Anum, Grishma Arun Kumar, Mehal Patel, Jolly Yan

"""
import load_data
import visualization_network
import visualization_bokeh
import entities


def load_welcome_message() -> None:
    """The intial message that will be presented when the file is run"""

    print("----- Beyond the Podium: A battle of dominance between F1’s greatest -----")
    print("*  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *")
    print(" *  *  *  *  *  *   *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  * \n")

    print("Every year since 1950, Formula 1 has hosted around 20 races (Grand Prixs) worldwide, "
          "with approximately 20 drivers competing in each\n")

    print("Our program helps to measure the relative dominance of Formula 1 drivers.")


def choose_drivers(original_graph: entities.Graph) -> tuple[int, int]:
    """Visualize the networkx for a single chosen driver 1, and allow for choosing driver 2"""
    available_codes = original_graph.get_dict_of_driver_names()
    available_names = available_codes.values()

    driver1 = input("\nEnter name of the first driver you would like to compare: ").lower().strip()
    while driver1 not in available_names and driver1 not in available_codes and driver1 != 'exit':
        print("That was an invalid name; try again.")
        driver1 = input("\nEnter name: ").lower().strip()

    if driver1 == 'exit':
        return -1, -1

    if driver1 in available_codes:
        driver1, driver1_code = available_codes[driver1], driver1
    else:
        driver1_code = original_graph.get_driver(driver1).driver_id

    single_driver_networkx_graph = visualization_network.create_single_driver_graph(original_graph, driver1)
    visualization_network.visualize_graph(single_driver_networkx_graph)

    driver2 = input("\nEnter name of the second driver you would like to compare "
                    "(NOTE: Cannot be the same as driver 1): ").lower().strip()

    while ((driver2 not in available_names and driver2 not in available_codes) or
           (driver2 == driver1 or driver2 == driver1_code)):
        if driver2 == 'exit':
            return -1, -1
        print("That was an invalid name; try again.")
        driver2 = input("\nEnter name: ").lower().strip()

    if driver2 in available_codes:
        driver2 = available_codes[driver2]

    driver1_id = original_graph.get_driver(driver1).driver_id
    driver2_id = original_graph.get_driver(driver2).driver_id

    return driver1_id, driver2_id


if __name__ == "__main__":
    graph = load_data.load_f1_data('Dataset/drivers.csv', 'Dataset/races.csv', 'Dataset/results.csv',
                                   'Dataset/sprint_results.csv')

    load_welcome_message()
    ongoing = True
    available_options = ['(a)', '(b)', 'exit']

    while ongoing:
        print("You can choose from the following commands:")
        print("- Show all drivers (A)")
        print("- Enter driver 1 to compare (B)")
        print("- Exit")

        choice = input("\nEnter action: ").lower().strip()
        while choice not in available_options:
            print("That was an invalid action; try again.")
            choice = input("\nEnter action: ").lower().strip()

        if choice == 'exit':
            print("Thank you for using our project")
            ongoing = False

        elif choice == '(a)':
            nx_graph = visualization_network.create_entire_graph(graph)
            visualization_network.visualize_graph(nx_graph)

        else:
            driver1_ID, driver2_ID = choose_drivers(graph)
            if driver1_ID == -1 and driver2_ID == -1:
                print("Thank you for using our project")
                ongoing = False
            else:
                d1 = graph.get_driver_by_id(driver1_ID)
                d2 = graph.get_driver_by_id(driver2_ID)

                stats = graph.compute_head_to_head(d1, d2)
                common_races = graph.get_shared_races(d1, d2)

                # printing stats in the console in order to compare with visualization
                print("\n" + "=" * 60)
                print(f"\nHEAD-TO-HEAD STATS: {len(common_races)} shared races")
                print("-" * 50)
                print(f"{'Metric':<20} | {d1.name:<15} | {d2.name:<15}")
                print("-" * 60)
                for metric, (p1, p2) in stats.items():
                    print(f"{metric:<20} | {p1:>14.1f}% | {p2:>14.1f}%")

                print("=" * 60)
                visualization_bokeh.bar_chart(graph, driver1_ID, driver2_ID)
