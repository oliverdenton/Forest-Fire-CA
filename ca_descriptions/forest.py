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

from capyle.ca import Grid2D, Neighbourhood, CAConfig, randomise2d
import capyle.utils as utils
import numpy as np


def transition_func(grid, neighbourstates, neighbourcounts):
    # dead = state == 0, live = state == 1
    # unpack state counts for state 0 and state 1
    # dead_neighbours, live_neighbours = neighbourcounts
    # # create boolean arrays for the birth & survival rules
    # # if 3 live neighbours and is dead -> cell born
    # birth = (live_neighbours == 3) & (grid == 0)
    # # if 2 or 3 live neighbours and is alive -> survives
    # survive = ((live_neighbours == 2) | (live_neighbours == 3)) & (grid == 1)
    # # Set all cells to 0 (dead)
    # grid[:, :] = 0
    # # Set cells to 1 where either cell is born or survives
    # grid[birth | survive] = 1
    return grid


def setup(args):
    config_path = args[0]
    config = utils.load(config_path)
    # ---THE CA MUST BE RELOADED IN THE GUI IF ANY OF THE BELOW ARE CHANGED---
    config.title = "Forest Fire Simulation"
    config.dimensions = 2
    #Comment what states mean
    states = {"B": 0, "C": 1, "DF": 2, "L": 3, "CS": 4, "C-B": 5, "DF-B": 6, "L-B": 7, "CS-B": 8}
    
    # States: 0 = Burnt, 1 = Chaparral, 2 = Lake, 3 = Forest, 4 = Canyon, 
    #         5 = Chaparral-Burning, 6 = Forest-Burning, 7 = Canyon-Burning, 8 = Town
    config.states = (0,1,2,3,4,5,6,7,8)
    # ------------------------------------------------------------------------

    # ---- Override the defaults below (these may be changed at anytime) ----
    config.state_colors = [(0.18, 0.09, 0), (0.8, 0.79, 0),(0, 0.68, 0.93), (0.3, 0.39, 0.16), (0.99,0.99, 0), 
                           (1, 0, 0),(1, 0, 0), (1, 0, 0), (0,0,0)]

    config.num_generations = 150
    config.grid_dims = (20,20)
    grid = np.array([[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                    [1,1,1,1,1,4,3,3,1,1,1,1,1,1,1,1,1,1,1,1],
                    [1,1,1,1,1,4,3,3,1,1,1,1,1,1,1,1,1,1,1,1],
                    [1,1,1,1,1,4,3,3,1,1,1,1,1,1,1,1,1,1,1,1],
                    [1,1,1,1,1,4,3,3,1,1,1,1,1,1,1,1,1,1,1,1],
                    [1,1,1,2,1,4,3,3,1,1,1,1,1,1,1,1,1,1,1,1],
                    [1,1,1,2,1,4,3,3,1,1,1,1,1,1,1,1,1,1,1,1],
                    [1,1,1,1,3,4,3,3,1,1,1,1,1,1,1,1,1,1,1,1],
                    [1,1,1,1,3,4,3,3,1,1,1,1,1,1,1,1,1,1,1,1],
                    [1,1,1,1,3,4,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
                    [1,1,1,1,3,4,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
                    [1,1,1,1,3,4,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                    [1,1,1,1,3,4,1,1,1,1,1,1,2,2,2,2,2,2,1,1],
                    [1,1,1,1,3,4,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                    [1,1,1,1,3,4,1,1,1,1,8,1,1,1,1,1,1,1,1,1],
                    [1,1,1,1,1,4,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                    [1,1,1,1,1,4,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]])

    config.set_initial_grid(grid)
    # ----------------------------------------------------------------------

    if len(args) == 2:
        config.save()
        sys.exit()

    return config


def main():
    # Open the config object
    config = setup(sys.argv[1:])

    # Create grid object
    grid = Grid2D(config, transition_func)

    # Run the CA, save grid state every generation to timeline
    timeline = grid.run()

    # save updated config to file
    config.save()
    # save timeline to file
    utils.save(timeline, config.timeline_path)


if __name__ == "__main__":
    main()
