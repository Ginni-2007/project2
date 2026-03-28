"""
# TODO : still need to add
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
    available_names = original_graph.get_list_of_driver_names()

    driver1 = input("\nEnter name of the first driver you would like to compare: ").lower().strip()
    while driver1 not in available_names:
        print("That was an invalid name; try again.")
        driver1 = input("\nEnter name: ").lower().strip()

    single_driver_networkx_graph = visualization_network.create_single_driver_graph(original_graph, driver1)
    visualization_network.visualize_graph(single_driver_networkx_graph)

    driver2 = input("\nEnter name of the second driver you would like to compare "
                    "(NOTE: Cannot be the same as driver 1): ").lower().strip()
    while driver2 not in available_names or driver2 == driver1:
        print("That was an invalid name; try again.")
        driver2 = input("\nEnter name: ").lower().strip()

    driver1_id = original_graph.get_driver(driver1).driver_id
    driver2_id = original_graph.get_driver(driver2).driver_id

    return driver1_id, driver2_id


if __name__ == "__main__":
    graph = load_data.load_f1_data('Dataset/drivers.csv', 'Dataset/races.csv', 'Dataset/results.csv')

    load_welcome_message()
    ongoing = True
    available_options = ['(a)', '(b)', '(c)']

    while ongoing:
        print("You can choose from the following commands:")
        print("- Show all drivers (A)")
        print("- Enter driver 1 to compare (B)")
        print("- Exit (C)")

        choice = input("\nEnter action: ").lower().strip()
        while choice not in available_options:
            print("That was an invalid action; try again.")
            choice = input("\nEnter action: ").lower().strip()

        if choice == '(c)':
            ongoing = False

        elif choice == '(a)':
            nx_graph = visualization_network.create_entire_graph(graph)
            visualization_network.visualize_graph(nx_graph)

        else:
            driver1_ID, driver2_ID = choose_drivers(graph)
            # TODO: add the visualize bokeh componenet in here


