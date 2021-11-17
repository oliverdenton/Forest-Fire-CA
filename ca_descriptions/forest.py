# Name: Conway's game of life
# Dimensions: 2

# --- Set up executable path, do not edit ---
import sys
import inspect
this_file_loc = (inspect.stack()[0][1])
main_dir_loc = this_file_loc[:this_file_loc.index('ca_descriptions')]
sys.path.append(main_dir_loc)
sys.path.append(main_dir_loc + 'capyle')
sys.path.append(main_dir_loc + 'capyle/ca')
sys.path.append(main_dir_loc + 'capyle/guicomponents')
# ---

import numpy as np
import capyle.utils as utils
from capyle.ca import Grid2D, Neighbourhood, CAConfig, randomise2d
import random

# Returns True probability % of the time
def decision(probability):
    return random.random() < probability
    
# Returns cells which will burn at next time step
def next_burning_cells(possible_cells_to_burn, probability):
    for ix,iy in np.ndindex(possible_cells_to_burn.shape):
        if possible_cells_to_burn[ix,iy]:
            if decision(probability):
                possible_cells_to_burn[ix,iy] = True
            else:
                possible_cells_to_burn[ix,iy] = False
    return possible_cells_to_burn

def transition_func(grid, neighbourstates, neighbourcounts, decaygrid):

    fuel = {"canyon": 1, "chaparral": 4, "dense_forest":16}
    wind_direction = "NW"
    # unpack state counts for all states
    burnt, chaparral, lake, dense_forest, canyon, chaparral_burning, dense_forest_burning, canyon_buring, town = neighbourcounts
    all_burning_neighbours_counts = chaparral_burning + dense_forest_burning + canyon_buring
    # unpack the state arrays
    NW, N, NE, W, E, SW, S, SE = neighbourstates

    # randomly start fire at power plant location
    if decision(0.05) and np.all(grid[7:9,17:19] != 0):
        grid[7:9,17:19] = 5
        decaygrid[7:9, 17:19] = fuel.get("chaparral")

    more_than_1_neighbours_burning = (all_burning_neighbours_counts >= 1) # cells that have more than 1 neighbours which are burning
    
    # Canyon
    canyon_cells = (grid == 4) # find all canyon cell
    canyon_probability = 1 # Probability of canyon cell burning 
    canyon_possible_cells_to_burn = canyon_cells & more_than_1_neighbours_burning # Canyon cells which have at least 1 burning neighbour
    canyon_next_burning_cells = next_burning_cells(canyon_possible_cells_to_burn, canyon_probability)
    grid[canyon_next_burning_cells] = 7

    # Chaparral 
    chaparral_cells = (grid == 1) # find all chaparral cell
    chaparral_cells_probability = 0.4 # Probability of chaparral cell burning 
    chaparral_possible_cells_to_burn = chaparral_cells & more_than_1_neighbours_burning # chaparral cells which have at least 1 burning neighbour
    chaparral_next_burning_cells = next_burning_cells(chaparral_possible_cells_to_burn, chaparral_cells_probability)
    grid[chaparral_next_burning_cells] = 5

    # Dense Forest
    dense_forest_cells = (grid == 3) # find all dense_forest cell
    dense_forest_probability = 0.1 # Probability of dense forest cell burning 
    dense_forest_possible_cells_to_burn = dense_forest_cells & (more_than_1_neighbours_burning) # Dense Forest cells which have at least 1 burning neighbour
    dense_forest_next_burning_cells = next_burning_cells(dense_forest_possible_cells_to_burn, dense_forest_probability)
    grid[dense_forest_next_burning_cells] = 6


    # Decay
    burning_cells = (grid == 5) | (grid == 6) | (grid == 7)  # find burning chaparral cells
    decaygrid[burning_cells] -= 1 # decrease fuel in burning chapprall cells by 1

    # add initial fuel to decay grid
    decaygrid[canyon_next_burning_cells] = fuel.get("canyon")
    decaygrid[chaparral_next_burning_cells] = fuel.get("chaparral")
    decaygrid[dense_forest_next_burning_cells] = fuel.get("dense_forest")

    decayed_to_zero = (decaygrid == 0) # find those which have decayed to 0
    grid[decayed_to_zero] = 0 # switch their state to 0

    return grid

def setup(args):
    config_path = args[0]
    config = utils.load(config_path)
    # ---THE CA MUST BE RELOADED IN THE GUI IF ANY OF THE BELOW ARE CHANGED---
    config.title = "Forest Fire Simulation"
    config.dimensions = 2
    # Comment what states mean
    states = {"B": 0, "C": 1, "DF": 2, "L": 3, "CS": 4,
              "C-B": 5, "DF-B": 6, "L-B": 7, "CS-B": 8}

    # States: 0 = Burnt, 1 = Chaparral, 2 = Lake, 3 = Dense Forest, 4 = Canyon,
    #         5 = Chaparral-Burning, 6 = Dense Forest-Burning, 7 = Canyon-Burning, 8 = Town
    config.states = (0, 1, 2, 3, 4, 5, 6, 7, 8)
    # ------------------------------------------------------------------------

    # ---- Override the defaults below (these may be changed at anytime) ----
    config.state_colors = [(0.18, 0.09, 0), (0.8, 0.79, 0), (0, 0.68, 0.93), (0.3, 0.39, 0.16), (0.99, 0.99, 0),
                           (1, 0, 0), (1, 0, 0), (1, 0, 0), (0, 0, 0)]

    config.num_generations = 150
    config.grid_dims = (20, 20)
    grid = np.array([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 4, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 4, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 4, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 4, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 2, 1, 4, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 2, 1, 4, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 3, 4, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
                    [1, 1, 1, 1, 3, 4, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 3, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
                    [1, 1, 1, 1, 3, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
                    [1, 1, 1, 1, 3, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 3, 4, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 1, 1],
                    [1, 1, 1, 1, 3, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 3, 4, 1, 1, 1, 1, 8, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])

    config.set_initial_grid(grid)

    config.wrap = False
    # ----------------------------------------------------------------------

    if len(args) == 2:
        config.save()
        sys.exit()

    return config


def main():
    # Open the config object
    config = setup(sys.argv[1:])

    decaygrid = np.zeros(config.grid_dims)
    decaygrid.fill(-1)
    start = False
    # Create grid object
    grid = Grid2D(config, (transition_func, decaygrid))

    # Run the CA, save grid state every generation to timeline
    timeline = grid.run()

    # save updated config to file
    config.save()
    # save timeline to file
    utils.save(timeline, config.timeline_path)


if __name__ == "__main__":
    main()
