from cube_utils import create_cube, basic_cube, translate_path_for_gui, perform_move, save_cube
import numpy as np
from datetime import datetime
import time
import matplotlib.pyplot as plt


def init_cube(number_of_scrambles=5):
    N = 3
    curr = State()
    curr.cube = np.array(basic_cube)
    move_list = create_cube(number_of_scrambles, curr.cube)
    plt.show()
    return curr, move_list


def ida_solve_cube(curr):
    time.ctime()
    fmt = '%H:%M:%S'
    start = time.strftime(fmt)

    path_to_solution = ida(curr)
    path_for_gui = translate_path_for_gui(path_to_solution)
    print("path to solution", path_to_solution)

    time.ctime()
    end = time.strftime(fmt)
    print("Calculation time(sec):", datetime.strptime(end, fmt) - datetime.strptime(start, fmt))
    return path_for_gui[::-1]


class State:
    cube = None
    g = 0
    h = 0
    parent = None
    move = None


def goal_reached(curr):
    """
    This function checks if the goal was reached.
    and if so, write the goal state into the output file
    :param curr: current state
    :return: true if we reached the goal, else False
    """
    if curr.h != 0:
        return False

    # goal was reached, save it:
    try:
        file = open('output.txt', 'w')
        save_cube(file, curr.cube)
        return True

    except IOError:
        print("IO ERROR")


def check_repeat_family(state, parent):
    """
    this function checks if the state is a ascendant of the parent
    """
    current_state = parent.parent
    while current_state is not None:
        if np.array_equal(current_state.cube, state):
            return True
        current_state = current_state.parent

    return False


def check_repeat_frontier(state, frontier):
    """
    This function checks if the frontier contains the state
    """
    for curr in frontier:
        if np.array_equal(curr.cube, state):
            return True

    return False


def ida(init_state):
    # todo why we calculating h in the rote node.

    init_state.h = corner_edge_sum_max(init_state.cube)
    cost_limit = init_state.h
    expended_nodes = 0
    frontier = list()
    branching_factors = list()

    while True:
        minimum = None
        frontier.append(init_state)
        path_to_solution = []

        while len(frontier) != 0:
            curr = frontier.pop()

            if goal_reached(curr):
                print('Goal Height:', curr.g)
                print('Branching Factor:', sum(branching_factors)/len(branching_factors))
                while curr is not None:
                    if curr.move is not None:
                        path_to_solution.append(curr.move)

                    curr = curr.parent
                print("Nodes Generated:", expended_nodes)
                return path_to_solution

            b = 0
            expended_nodes = expended_nodes + 12
            for i in range(12):
                new = State()
                new.cube = np.array(curr.cube)
                new.g = curr.g + 1
                new.parent = curr
                new.move = perform_move(new.cube, i + 1, 0)[1]
                new.h = corner_edge_sum_max(new.cube)

                if new.g + new.h > cost_limit:
                    if minimum is None or new.g + new.h < minimum:
                        minimum = new.g + new.h
                    continue
                if curr.parent is not None and (check_repeat_family(new.cube, curr) or check_repeat_frontier(new.cube, frontier)):
                    continue
                frontier.append(new)

                b = b + 1
            if b != 0:
                branching_factors.append(b)

        cost_limit = minimum


def calculate_distance(c1, c2):
    return abs(c1[0] - c2[0]) + abs(c1[1] - c2[1]) + abs(c1[2] - c2[2])


def manhattan_distance(cube, i, z, corner):
    c1 = cube_array[i, z]
    center = None
    for c in [1, 4, 7, 10, 13, 16]:
        if cube[i, z] == cube[c, 1]: # checks the colors, to know in which side of the original cube to compere to
            center = c
            break

    if corner:
        c2_list = [cube_array[center - 1, 0], cube_array[center - 1, 2], cube_array[center + 1, 0], cube_array[center + 1, 2]]
        d = []
        for c2 in c2_list:
            d.append(calculate_distance(c1, c2))

        return min(d)

    else:
        c2_list = [cube_array[center - 1, 1], cube_array[center, 0], cube_array[center, 2], cube_array[center + 1, 1]]
        d = []
        for c2 in c2_list:
            d.append(calculate_distance(c1, c2))

        return min(d)


""" for every cubie in the cube, the algorithm checks is color, goes to the border of that color in the initial cube 
 and and calculate the Manhatten dist by the numbers ( its the cord from 0- 2 in the border) from the border in the 
 current cube """
def corner_edge_sum_max(cube):
    corners = 0
    edges = 0
    for i in range(18):
        if i % 3 == 0 or i % 3 == 2:
            corners = corners + manhattan_distance(cube, i, 0, True) + manhattan_distance(cube, i, 2, True)
            edges = edges + manhattan_distance(cube, i, 1, False)
        else:
            edges = edges + manhattan_distance(cube, i, 0, False) + manhattan_distance(cube, i, 2, False)
    return max(corners / 12, edges / 8)


def corner_edge_sum_divide_by_4(cube):
    max_corners = 0
    max_edges = 0
    for i in range(18):
        temp_corers = 0
        temp_edges = 0
        if i % 3 == 0 or i % 3 == 2:
            max_corners = max_corners + manhattan_distance(cube, i, 0, True) + manhattan_distance(cube, i, 2, True)
            max_edges = max_edges + manhattan_distance(cube, i, 1, False)
        else:
            max_edges = max_edges + manhattan_distance(cube, i, 0, False) + manhattan_distance(cube, i, 2, False)


def kurf_h(cube):
    corners = 0
    edges_1 = 0
    edges_2 = 0
    for i in range(18):
        if i % 3 == 0 or i % 3 == 2:
            corners = corners + manhattan_distance(cube, i, 0, True) + manhattan_distance(cube, i, 2, True)
            if i % 3 == 0:
                edges_1 = edges_1 + manhattan_distance(cube, i, 1, False)
            else:
                edges_2 = edges_2 + manhattan_distance(cube, i, 1, False)

        else:
            edges_1 = edges_1 + manhattan_distance(cube, i, 0, False)
            edges_2 = edges_2 + manhattan_distance(cube, i, 2, False)
    return max(corners, edges_1, edges_2)

def sum_divided_by_eight(cube):
    corners = 0
    edges = 0
    for i in range(18):
        if i % 3 == 0 or i % 3 == 2:
            corners = corners + manhattan_distance(cube, i, 0, True) + manhattan_distance(cube, i, 2, True)
            edges = edges + manhattan_distance(cube, i, 1, False)
        else:
            edges = edges + manhattan_distance(cube, i, 0, False) + manhattan_distance(cube, i, 2, False)
    return (corners + edges) / 8




# todo: change this array to make it look better
cube_array = np.array([
    [[0, 0, 2], [1, 0, 2], [2, 0, 2]],  # 2 corners + 1 edge
    [[0, 0, 1], [1, 0, 1], [2, 0, 1]],  # center + 2 edge
    [[0, 0, 0], [1, 0, 0], [2, 0, 0]],  # 2 corners + 1 edge
    [[0, 0, 2], [0, 1, 2], [0, 2, 2]],  # 2 corners + 1 edge
    [[0, 0, 1], [0, 1, 1], [0, 2, 1]],  # center + 2 edge
    [[0, 0, 0], [0, 1, 0], [0, 2, 0]],  # 2 corners + 1 edge
    [[0, 0, 0], [1, 0, 0], [2, 0, 0]],  # 2 corners + 1 edge
    [[0, 1, 0], [1, 1, 0], [2, 1, 0]],  # center + 2 edge
    [[0, 2, 0], [1, 2, 0], [2, 2, 0]],  # 2 corners + 1 edge
    [[2, 0, 0], [2, 0, 1], [2, 0, 2]],  # 2 corners + 1 edge
    [[2, 1, 0], [2, 1, 1], [2, 1, 2]],  # center + 2 edge
    [[2, 2, 0], [2, 2, 1], [2, 2, 2]],  # 2 corners + 1 edge
    [[2, 0, 2], [1, 0, 2], [0, 0, 2]],  # 2 corners + 1 edge
    [[2, 1, 2], [1, 1, 2], [0, 1, 2]],  # center + 2 edge
    [[2, 2, 2], [1, 2, 2], [0, 2, 2]],  # 2 corners + 1 edge
    [[0, 2, 0], [1, 2, 0], [2, 2, 0]],  # 2 corners + 1 edge
    [[0, 2, 1], [1, 2, 1], [2, 2, 1]],  # center + 2 edge
    [[0, 2, 2], [1, 2, 2], [2, 2, 2]],  # 2 corners + 1 edge
])
