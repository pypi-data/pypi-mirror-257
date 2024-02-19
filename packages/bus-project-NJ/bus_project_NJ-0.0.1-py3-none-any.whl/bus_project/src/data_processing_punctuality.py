import os
import json
import matplotlib.pyplot as plt
from typing import Tuple
from helper_functions import create_directory, load_geojson

# Set the font styles for the plots to ensure consistency and cohesion
fontstyle_annotation = {'fontsize': 9,
                        'fontweight': 'bold', 'color': '#14333D'}

fontstyle_small = {'fontsize': 8, 'color': '#14333D'}

fontstyle_title = {'fontsize': 13, 'fontweight': 'bold', 'color': '#14333D'}

# Colours for each of the districts
colours = ['#3943B7', '#83C5BE', '#0CF574', '#617073', '#E29578', '#BF9ACA',
           '#EB5160', '#FF7F11', '#2AB7CA', '#7BD389', '#521945', '#9B7EDE',
           '#76E7CD', '#29335C', '#AF125A', '#C6BF06', '#35A7FF', '#706C61']


def convert_data(data: list) -> list:
    '''Converts the data from seconds to minutes and
    puts it into a dictionary
    '''

    new_data = []

    for info in data:
        info = info // 60

        new_data.append(info)

    return new_data


def get_percentage(data: list) -> float:
    '''Calculates the percentage of busses that are late in a district'''

    late = 0

    for info in data:
        if info > 5:
            late += 1

    return (late / len(data)) * 100


def plot_district(district: str, data: list, plot: plt.Axes,
                  colour: str, order: str) -> None:
    '''Plots the number of minutes late for a specific district'''

    frequencies = {}
    data = convert_data(data)

    for number in data:
        if number in frequencies:
            frequencies[number] += 1
        else:
            frequencies[number] = 1

    x = list(frequencies.keys())
    y = list(frequencies.values())

    plot.set_title(f'{district} #{order}', fontstyle_annotation)
    plot.set_xlabel('Number of minutes late', fontstyle_small)
    plot.set_ylabel('Frequency', fontstyle_small)

    # Each district has a different colour from the colours array
    plot.bar(x, y, color=colour)


def plot_warsaw(data, plot: plt.Axes) -> None:
    '''Plots the number of minutes late for all of Warsaw'''

    frequencies = {}

    for district in data:
        for number in convert_data(data[district]):
            if number in frequencies:
                frequencies[number] += 1
            else:
                frequencies[number] = 1

    x = list(frequencies.keys())
    y = list(frequencies.values())

    plot.set_title('Warsaw', fontstyle_annotation)
    plot.set_xlabel('Number of minutes late', fontstyle_small)
    plot.set_ylabel('Frequency', fontstyle_small)

    plot.bar(x, y)


def plot_district_percentage(districts, data, plot: plt.Axes) -> None:
    '''Plots the percentage of busses late in each district in one plot'''

    percentages = {}
    district_number = 0

    for district in districts:
        if district not in data:
            continue
        
        if len(data[district]) == 0:  # Avoids division by zero
            continue

        percentages[district_number +
                    1] = get_percentage(convert_data(data[district]))
        
        # Each district is assigned a number from 1 to 18
        district_number += 1  

    x = list(percentages.keys())
    y = list(percentages.values())

    plot.set_title(
        'The percentage of busses\nlate in each district',
        fontstyle_annotation)
    plot.set_xlabel('District number', fontstyle_small)
    plot.set_ylabel('Percentage', fontstyle_small)

    plot.bar(x, y, color=colours)


def configure_plot() -> Tuple[plt.Figure, plt.Axes]:
    '''Creates the appropriate figure and plot to plot the
    punctuality of Warsaw's busses
    '''

    figure, plot = plt.subplots(4, 5, figsize=(30, 20))
    figure.subplots_adjust(wspace=0.6, hspace=0.6)

    figure.suptitle(
        'The number of minutes late in Warsaw and all of Warsaw\'s districts',
        fontsize=16,
        fontweight='bold',
        fontdict=fontstyle_title,
        y=0.96)

    return figure, plot


def plot_lateness(data_set: int) -> None:
    '''Plots the number of minutes late for all of Warsaw and
    all of Warsaw's districts
    '''

    # Creates a directory for the plots if it does not already exist
    create_directory(data_set)

    try:
        with open(f'lateness_data/lateness_{data_set}.json', 'r') as file:
            lateness_data = json.load(file)
    except FileNotFoundError:
        print(f"ERROR: File lateness_data/lateness_{data_set}.json \
              does not exist")
        return

    districts_file = load_geojson('warszawa-dzielnice.geojson')

    districts = sorted([district['properties']['name']
                       for district in districts_file['features'][1:]])

    figure, plot = configure_plot()

    iter = 0

    for i in range(20):
        row = i // 5
        col = i % 5

        if i == 7:
            plot_warsaw(lateness_data, plot[row][col])
            continue

        if i == 12:
            plot_district_percentage(districts, lateness_data, plot[row][col])
            continue

        if districts[iter] in lateness_data:
            plot_district(districts[iter],
                        lateness_data[districts[iter]],
                        plot[row][col],
                        colours[iter],
                        f'{iter + 1}')

        iter += 1

    plt.get_current_fig_manager().full_screen_toggle()
    plt.savefig(f'plots/plots_{data_set}/Bus_punctuality_plot_{data_set}.png')
    