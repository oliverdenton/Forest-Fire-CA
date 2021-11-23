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
import math

# Returns True probability % of the time
def decision(probability):
    return random.random() < probability
    
# Returns cells which will burn at next time step
def next_burning_cells(possible_cells_to_burn, probability, cells_with_wind, cells_opposite_wind):
<<<<<<< HEAD
    WIND_FACTOR = 25 # 0%
=======
    WIND_FACTOR = 100 # 0%
>>>>>>> cf79c261e80e64fea31cf500010a5ad5c1ef2d27
    SEASON = "none"
    season_factor = {"winter":0.5, "summer":1.5, "autumn":1.1, "spring":0.9, "none":1}

    base_probability = probability

    for ix,iy in np.ndindex(possible_cells_to_burn.shape):
        # scale probability depending on wind direction
        temp_probability = base_probability
        if possible_cells_to_burn[ix,iy] and (cells_with_wind[ix,iy]):
            temp_probability = base_probability * (1-WIND_FACTOR)
        elif possible_cells_to_burn[ix,iy] and (cells_opposite_wind[ix,iy]):
            temp_probability = base_probability * (1+WIND_FACTOR)
        else:
            temp_probability = base_probability
        # scale probability depending on season
        temp_probability = temp_probability * season_factor[SEASON]
        if possible_cells_to_burn[ix,iy]:
            if decision(temp_probability):
                possible_cells_to_burn[ix,iy] = True
            else:
                possible_cells_to_burn[ix,iy] = False
    return possible_cells_to_burn

def transition_func(grid, neighbourstates, neighbourcounts, decaygrid):

    fuel = {"canyon": 1, "chaparral": 12, "dense_forest":120, "town":-1}
<<<<<<< HEAD
    wind_direction = "SE"
=======
    wind_direction = "NE"
>>>>>>> cf79c261e80e64fea31cf500010a5ad5c1ef2d27

    # unpack state counts for all states
    burnt, chaparral, lake, dense_forest, canyon, chaparral_burning, dense_forest_burning, canyon_buring, town, town_burning = neighbourcounts
    all_burning_neighbours_counts = chaparral_burning + dense_forest_burning + canyon_buring + town_burning
    # unpack the state arrays
    NW, N, NE, W, E, SW, S, SE = neighbourstates
    wind_with= {"NW":(SE, S , E), "N": (S , SE , SW), "NE":(SW,S,W), "W":(E,NE,SE), "E":(W,NW,SW), "SW":(NE,N,E), "S":(N,NE,NW), "SE":(NW,W,N)}
    wind_opposite= {"NW":(NW,N,W), "N":(N,NE,NW), "NE":(NE,E,N), "W":(W,SW,SE), "E":(E,SE,NE), "SW":(SW,W,S), "S":(S,SE,SW), "SE":(SE,S,E)}

    sf = int(grid.shape[0] / 40)

    # Start fire at power plant location, with a changable probability
    if decision(0) and np.all(grid[sf*14:sf*18,sf*34:sf*38] == 1):
        grid[sf*14:sf*18,sf*34:sf*38] = 5
        decaygrid[sf*14:sf*18, sf*34:sf*38] = fuel.get("chaparral")

    # Start fire at incinerator location, with a changable probability
    if decision(1) and np.all(grid[sf*14:sf*18,sf*2:sf*6] == 1):
        grid[sf*14:sf*18,sf*2:sf*6] = 5
        decaygrid[sf*14:sf*18, sf*2:sf*6] = fuel.get("chaparral")

    more_than_1_neighbours_burning = (all_burning_neighbours_counts >= 1) # cells that have more than 1 neighbours which are burning
    cells_with_wind = (wind_with[wind_direction][0] == 5 ) | (wind_with[wind_direction][0] == 6) | (wind_with[wind_direction][0] == 7) | (wind_with[wind_direction][0] == 9)
    cells_opposite_wind = (wind_opposite[wind_direction][0] == 5) | (wind_opposite[wind_direction][0] == 6) | (wind_opposite[wind_direction][0] == 7) | (wind_opposite[wind_direction][0] == 9)

    # Canyon
    canyon_cells = (grid == 4) # find all canyon cell
    canyon_probability = 0.8 # Probability of canyon cell burning 
    canyon_possible_cells_to_burn = canyon_cells & more_than_1_neighbours_burning # Canyon cells which have at least 1 burning neighbour
    canyon_next_burning_cells = next_burning_cells(canyon_possible_cells_to_burn, canyon_probability, cells_with_wind, cells_opposite_wind)
    grid[canyon_next_burning_cells] = 7

    # Chaparral 
    chaparral_cells = (grid == 1) # find all chaparral cell
    chaparral_cells_probability = 0.4 # Probability of chaparral cell burning 
    chaparral_possible_cells_to_burn = chaparral_cells & more_than_1_neighbours_burning # chaparral cells which have at least 1 burning neighbour
    chaparral_next_burning_cells = next_burning_cells(chaparral_possible_cells_to_burn, chaparral_cells_probability, cells_with_wind, cells_opposite_wind)
    grid[chaparral_next_burning_cells] = 5

    # Dense Forest
    dense_forest_cells = (grid == 3) # find all dense_forest cell
    dense_forest_probability = 0.1 # Probability of dense forest cell burning 
    dense_forest_possible_cells_to_burn = dense_forest_cells & (more_than_1_neighbours_burning) # Dense Forest cells which have at least 1 burning neighbour
    dense_forest_next_burning_cells = next_burning_cells(dense_forest_possible_cells_to_burn, dense_forest_probability,  cells_with_wind, cells_opposite_wind)
    grid[dense_forest_next_burning_cells] = 6

    # Town
    town_cells = (grid == 8) # find all town cell
    town_probability = 1 # Probability of town cell burning 
    town_possible_cells_to_burn = town_cells & (more_than_1_neighbours_burning) # Town cells which have at least 1 burning neighbour
    town_next_burning_cells = next_burning_cells(town_possible_cells_to_burn, town_probability,  cells_with_wind, cells_opposite_wind)
    grid[town_next_burning_cells] = 9


    # Decay
    burning_cells = (grid == 5) | (grid == 6) | (grid == 7) | (grid == 9) # find burning cells
    decaygrid[burning_cells] -= 1 # decrease fuel in burning chapprall cells by 1

    # add initial fuel to decay grid
    decaygrid[canyon_next_burning_cells] = fuel.get("canyon")
    decaygrid[chaparral_next_burning_cells] = fuel.get("chaparral")
    decaygrid[dense_forest_next_burning_cells] = fuel.get("dense_forest")
    decaygrid[town_next_burning_cells] = fuel.get("town")

    decayed_to_zero = (decaygrid == 0) # find those which have decayed to 0
    grid[decayed_to_zero] = 0 # switch their state to 0

    return grid

def setup(args):
    config_path = args[0]
    config = utils.load(config_path)
    # ---THE CA MUST BE RELOADED IN THE GUI IF ANY OF THE BELOW ARE CHANGED---
    config.title = "Forest Fire Simulation"
    config.dimensions = 2

    # States: 0 = Burnt, 1 = Chaparral, 2 = Lake, 3 = Dense Forest, 4 = Canyon,
    #         5 = Chaparral-Burning, 6 = Dense Forest-Burning, 7 = Canyon-Burning, 8 = Town, 9 = Town Burning
    config.states = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
    # ------------------------------------------------------------------------

    # ---- Override the defaults below (these may be changed at anytime) ----
    config.state_colors = [(0.18, 0.09, 0), (0.8, 0.79, 0), (0, 0.68, 0.93), (0.3, 0.39, 0.16), (0.99, 0.99, 0),
                           (1, 0, 0), (1, 0, 0), (1, 0, 0), (0, 0, 0), (1, 0.53, 0)]

    config.num_generations = 300
    
    grid = np.array([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 

                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],

                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 4, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 4, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],

                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 4, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 4, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],

                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 4, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 4, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],

                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 4, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 4, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],

                     [1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 4, 4, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 4, 4, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],

                     [1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 4, 4, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 4, 4, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],

                     [1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 4, 4, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
                     [1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 4, 4, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 

                     [1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 4, 4, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 4, 4, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 

                     [1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
                     [1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],

                     [1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
                     [1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],

                     [1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 4, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 4, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],

                     [1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 4, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 4, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1],

                     [1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 4, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 4, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],

                                      
                     [1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 4, 4, 1, 1, 1, 1, 1, 1, 1, 1, 8, 8, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 4, 4, 1, 1, 1, 1, 1, 1, 1, 1, 8, 8, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],

                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],

                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],

                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],

                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])

    # Standard Grid size is 40x40, scale up by scale factor sf:
    sf = 1
    new_grid = np.kron(grid, np.ones((sf,sf)))
    config.grid_dims = (40*sf, 40*sf)

    config.set_initial_grid(new_grid)

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
