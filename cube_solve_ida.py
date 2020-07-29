from cube_utils import create_cube, basic_cube, translate_path_for_gui, perform_move, save_cube,\
    PrintCube, print_cube_per_size, cube_size
from reinforcement_learning_solver import *
import numpy as np
from datetime import datetime
import time
import matplotlib.pyplot as plt
from plot_results import *

def read_cube_from_file(cur_cube, cube_file='input1.txt'):
    cube_to_create = open(cube_file)
    indexes = [0, 1, 2, 3, 6, 9, 12, 4, 7, 10, 13, 5, 8, 11, 14, 15, 16, 17]
    index = 0
    for line in cube_to_create:
        line = line.replace(' ', '')
        for row in line.split('['):
            if len(row) != 0:
                i = indexes[index]
                cur_cube.cube[i, 0] = row[1]
                cur_cube.cube[i, 1] = row[4]
                cur_cube.cube[i, 2] = row[7]
                index = index + 1


def run_without_gui(number_of_scrambles=6, from_file=None):
    if from_file:
        curr = State()
        curr.cube = np.array(basic_cube)
        read_cube_from_file(curr, cube_file='input1.txt')
        print_cube_per_size(curr.cube)
    else:
        curr, move_list, moves_by_numbers = init_cube(number_of_scrambles)

    expended_nodes_list = []
    heuristic = []

    print("corner edge sum max:")
    sol_corner_edge_sum_max, expended_nodes = ida_solve_cube(curr, corner_edge_sum_max)
    heuristic.append("corner edge sum max")
    expended_nodes_list.append(expended_nodes)

    print("sum divided by eight solution:")
    sol_sum_divided_by_eight, expended_nodes = ida_solve_cube(curr, sum_divided_by_eight)
    heuristic.append("sum divided by eight")
    expended_nodes_list.append(expended_nodes)

    print("korf solution:")
    sol_kurf, expended_nodes = ida_solve_cube(curr, kurf_h)
    heuristic.append("korf")
    expended_nodes_list.append(expended_nodes)

    print("colors solution:")
    sol_colors, expended_nodes = ida_solve_cube(curr, color_heuristic)
    heuristic.append("colors")
    expended_nodes_list.append(expended_nodes)

    print("reinforcement learning solution")
    sol_reinforcement_learning = solve_reinforcement_learning(moves_by_numbers)

    expanded_nodes(heuristic, expended_nodes_list)

def init_cube(number_of_scrambles=7):
    N = 3
    curr = State()
    curr.cube = np.array(basic_cube)
    move_list, moves_by_numbers = create_cube(number_of_scrambles, curr.cube)
    plt.show()
    return curr, move_list, moves_by_numbers


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
        print("solution: \n")
        print_cube_per_size(curr.cube)
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


def ida(init_state, heuristic):
    # corner_edge_sum_max todo (adi) delete this comment
    # todo why we calculating h in the rote node.

    init_state.h = heuristic(init_state.cube)
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
                return path_to_solution, expended_nodes

            b = 0
            expended_nodes = expended_nodes + 12
            for i in range(12):
                new = State()
                new.cube = np.array(curr.cube)
                new.g = curr.g + 1
                new.parent = curr
                new.move = perform_move(new.cube, i + 1, 0)[1]
                new.h = heuristic(new.cube)

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


# def corner_edge_sum_divide_by_4(cube):
#     # todo - ERROR!
#     max_corners = 0
#     max_edges = 0
#     for i in range(18):
#         temp_corers = 0
#         temp_edges = 0
#         if i % 3 == 0 or i % 3 == 2:
#             max_corners = max_corners + manhattan_distance(cube, i, 0, True) + manhattan_distance(cube, i, 2, True)
#             max_edges = max_edges + manhattan_distance(cube, i, 1, False)
#         else:
#             max_edges = max_edges + manhattan_distance(cube, i, 0, False) + manhattan_distance(cube, i, 2, False)


def kurf_h(cube):
    # TODO - run forever :(

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
    return max(corners/8, edges_1/4, edges_2/4)


def sum_divided_by_eight(cube):
    # todo - this heuristic works, great!
    corners = 0
    edges = 0
    for i in range(18):
        if i % 3 == 0 or i % 3 == 2:
            corners = corners + manhattan_distance(cube, i, 0, True) + manhattan_distance(cube, i, 2, True)
            edges = edges + manhattan_distance(cube, i, 1, False)
        else:
            edges = edges + manhattan_distance(cube, i, 0, False) + manhattan_distance(cube, i, 2, False)
    return (corners + edges) / 8


def color_heuristic(cube):
    """
    count the number of colors that different with goal.
    sometimes return non optimal solution
    """
    count = 0
    for i in range(6):
        color = cube[i*cube_size+1][1]
        for j in range(cube_size):
            for k in range(cube_size):
                if cube[i*cube_size+j][k] != color:
                    count += 1
    return count / 8


def ida_solve_cube(curr, heuristic=sum_divided_by_eight):
    time.ctime()
    fmt = '%H:%M:%S'
    start = time.strftime(fmt)

    path_to_solution, expended_nodes = ida(curr, heuristic)
    path_for_gui = translate_path_for_gui(path_to_solution)
    print("path to solution", path_to_solution)

    time.ctime()
    end = time.strftime(fmt)
    print("Calculation time(sec):", datetime.strptime(end, fmt) - datetime.strptime(start, fmt))

    return path_for_gui[::-1], expended_nodes





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


# cube_array_4 = np.array([
#     [0, 0, 3], [1, 0, 3], [2, 0, 3], [3, 0, 3],
#      [0, 0, 2], [1, 0, 2], [2, 0, 2], [3, 0, 2],
#      [[0, 0, 1], [1, 0, 1], [2, 0, 1], [3, 0, 1],
#     [[0, 0, 0], [1, 0, 0], [2, 0, 0], [3, 0, 0]],
#
#     [[0, 0, 2], [0, 1, 2], [0, 2, 2]],  # 2 corners + 1 edge
#     [[0, 0, 1], [0, 1, 1], [0, 2, 1]],  # center + 2 edge
#     [[0, 0, 0], [0, 1, 0], [0, 2, 0]],  # 2 corners + 1 edge
#
#     [[0, 0, 0], [1, 0, 0], [2, 0, 0]],  # 2 corners + 1 edge
#     [[0, 1, 0], [1, 1, 0], [2, 1, 0]],  # center + 2 edge
#     [[0, 2, 0], [1, 2, 0], [2, 2, 0]],  # 2 corners + 1 edge
#
#     [[2, 0, 0], [2, 0, 1], [2, 0, 2]],  # 2 corners + 1 edge
#     [[2, 1, 0], [2, 1, 1], [2, 1, 2]],  # center + 2 edge
#     [[2, 2, 0], [2, 2, 1], [2, 2, 2]],  # 2 corners + 1 edge
#
#     [[2, 0, 2], [1, 0, 2], [0, 0, 2]],  # 2 corners + 1 edge
#     [[2, 1, 2], [1, 1, 2], [0, 1, 2]],  # center + 2 edge
#     [[2, 2, 2], [1, 2, 2], [0, 2, 2]],  # 2 corners + 1 edge
#     [[0, 2, 0], [1, 2, 0], [2, 2, 0]],  # 2 corners + 1 edge
#     [[0, 2, 1], [1, 2, 1], [2, 2, 1]],  # center + 2 edge
#     [[0, 2, 2], [1, 2, 2], [2, 2, 2]],  # 2 corners + 1 edge
# ])


run_without_gui(6)