import helper_functions
import data_processing_punctuality
import data_processing_speed
import data_processing_theaters


def analyze_all(data_set: int, streets: bool = False) -> None:
    '''Analyzes the data from the given data set and plots the results'''

    # Checks whether the function call is valid, ie. whether the data
    # set exists and whether the data set has the required data
    valid_call = helper_functions.check_validity_of_function_call(
        data_set, streets, True)

    if not valid_call:
        raise ValueError("Invalid function call")

    data_processing_theaters.plot_theaters_map(data_set)

    analyze_punctuality(data_set, False)
    analyze_speed(data_set, streets, False)


def analyze_speed(data_set: int, streets: bool = False,
                  check_validity: bool = True) -> None:
    '''Only analyzes the speed of the busses in the given data
    set and plots the results
    '''

    if check_validity:
        valid_call = helper_functions.check_validity_of_function_call(
            data_set, streets, False)

        if not valid_call:
            raise ValueError("Invalid function call")

    if streets:
        data_processing_speed.plot_street_percentage(data_set)

    data_processing_speed.plot_district_percentage(data_set)
    data_processing_speed.plot_percentage_per_district(data_set)
    data_processing_speed.plot_number_of_infractions(data_set)
    data_processing_speed.draw_map(data_set)


def analyze_punctuality(data_set: int, check_validity: bool = True) -> None:
    '''Only analyzes the punctuality of the busses in the given data'''

    if check_validity:
        valid_call = helper_functions.check_validity_of_function_call(
            data_set, False, True)

        if not valid_call:
            raise ValueError("Invalid function call")

    data_processing_punctuality.plot_lateness(data_set)


def analyze_theaters(data_set: int, check_validity: bool = True) -> None:
    '''Only analyzes the theaters in the given data set
    and plots the results
    '''

    if check_validity:
        valid_call = helper_functions.check_validity_of_function_call(
            data_set, False, False)

        if not valid_call:
            raise ValueError("Invalid function call")

    data_processing_theaters.plot_theaters_map(data_set)
    