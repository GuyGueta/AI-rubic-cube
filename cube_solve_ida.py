from cube_utils import create_cube, basic_cube, translate_path_for_gui, perform_move, save_cube,\
    print_cube_per_size, cube_size
from reinforcement_learning_solver import *

from group_theory_solution import solve_with_group_theory
from datetime import datetime
import time
from plot_results import *


CUBE_CENTERS_DICT_4 = {'W': 1, 'B': 5, 'R': 9, 'G': 13, 'O': 17, 'Y': 21}
CUBE_BORDER_INDEX_4 = {3: 0, 7: 4, 11: 8, 15: 12, 19: 16, 23: 20}
CUBE_COLOR_CHOSEN_4 = {'W': False, 'B': False, 'R': False, 'G': False, 'O': False, 'Y': False}
CUBE_BORDER_CENTERS_INDEX_4 = {3: 1, 7: 5, 11: 9, 15: 13, 19: 17, 23: 21}


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

    if cube_size == 3:
        print("reinforcement learning solution")
        sol_reinforcement_learning = solve_reinforcement_learning(moves_by_numbers)
        print("Group theory solution:")
        group_theory_solution = solve_with_group_theory(curr)
        print("number of steps: ", len(group_theory_solution))
        print("path to solution: ", group_theory_solution)

    expanded_nodes(heuristic, expended_nodes_list)


def init_cube(number_of_scrambles=6):
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
    centers = {}


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


def ida(init_state, heuristic, is3on3=True):
    if is3on3:
        actions_len = 12
    else:
        actions_len = 24
        init_state.centers = find_centers_for_cube(init_state.cube)
        print(init_state.centers)
    init_state.h = heuristic(init_state, is3on3)
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
            # print_cube_per_size(curr.cube)
            # print(curr.h)

            if goal_reached(curr):
                print('Goal Height:', curr.g)
                if len(branching_factors) != 0:
                    print('Branching Factor:', sum(branching_factors)/len(branching_factors))
                while curr is not None:
                    if curr.move is not None:
                        path_to_solution.append(curr.move)

                    curr = curr.parent
                print("Nodes Generated:", expended_nodes)
                return path_to_solution, expended_nodes

            b = 0
            expended_nodes = expended_nodes + actions_len
            for i in range(actions_len):
                new = State()
                new.cube = np.array(curr.cube)
                new.g = curr.g + 1
                new.parent = curr
                new.move = perform_move(new.cube, i + 1, 0)[1]
                if not is3on3:
                    new.centers = init_state.centers
                new.h = heuristic(new, is3on3)
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


def manhattan_distance(cube, i, z, corner, is_3on3=True):
    if is_3on3:
        return manhattan_distance_3(cube, i, z, corner)
    else:
        return manhattan_distance_4(cube, i, z, corner)


def manhattan_distance_center(state, i, z):
    cube = state.cube
    centers_dict = state.centers
    c1 = cube_array_4[i, z]
    center = centers_dict[cube[i, z]]
    c2_list = [cube_array_4[center, 1], cube_array_4[center, 2], cube_array_4[center + 1, 1],
               cube_array_4[center + 1, 2]]
    d = []
    for c2 in c2_list:
        d.append(calculate_distance(c1, c2))
    return min(d)



def manhattan_distance_4(state, i, z, corner):
    cube = state.cube
    centers_dict = state.centers
    c1 = cube_array_4[i, z]
    center = centers_dict[cube[i, z]]
    if corner:
        c2_list = [cube_array_4[center - 1, 0], cube_array_4[center - 1, 3], cube_array_4[center + 2, 0],
                   cube_array_4[center + 2, 3]]
        d = []
        for c2 in c2_list:
            d.append(calculate_distance(c1, c2))

        return min(d)
    else:
        c2_list = [cube_array_4[center - 1, 1], cube_array_4[center - 1, 2], cube_array_4[center + 1, 0],
                   cube_array_4[center, 0], cube_array_4[center, 3], cube_array_4[center + 1, 3],
                   cube_array_4[center + 2, 1], cube_array_4[center + 2, 2]]
        d = []
        for c2 in c2_list:
            d.append(calculate_distance(c1, c2))
        return min(d)


def get_center(index):
    for num in CUBE_BORDER_CENTERS_INDEX_4.keys():
        if index <= num:
            return CUBE_BORDER_CENTERS_INDEX_4[num]


def find_centers_for_cube(cube):
    border_color_dict = {'W': 0, 'B': 0, 'R': 0, 'G': 0, 'O': 0, 'Y': 0}
    is_colored_dict = {'W': False, 'B': False, 'R': False, 'G': False, 'O': False, 'Y': False}
    index = 0
    while index < 24:
        calc_center_index(index, cube, border_color_dict, is_colored_dict)
        index = index + 4
    return border_color_dict


def calc_center_index(index, cube, border_color_dict,  is_colored_dict):
    border_start = 0
    for num in CUBE_BORDER_INDEX_4.keys():
        if index <= num:
            border_start = CUBE_BORDER_INDEX_4[num]
            break
    max_color = find_max_color(border_start, cube, is_colored_dict)
    border_color_dict[max_color] = get_center(index)


def find_max_color(border_start, cube,  is_colored_dict):
    counter_dict = {'W': 0, 'B': 0, 'R': 0, 'G': 0, 'O': 0, 'Y': 0}
    for i in range(border_start, border_start + 4):
        for j in range(4):
            counter_dict[cube[i, j]] += 1
    max_color = max(counter_dict, key=counter_dict.get)
    while is_colored_dict[max_color]:
        counter_dict[max_color] = 0
        max_color = max(counter_dict, key=counter_dict.get)
    is_colored_dict[max_color] = True
    return max_color


def manhattan_distance_3(cube, i, z, corner):
    c1 = cube_array[i, z]
    center = None
    for c in [1, 4, 7, 10, 13, 16]:
        if cube[i, z] == cube[c, 1]:  # checks the colors, to know in which side of the original cube to compere to
            center = c
            break

    if corner:
        c2_list = [cube_array[center - 1, 0], cube_array[center - 1, 2], cube_array[center + 1, 0],
                   cube_array[center + 1, 2]]
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


def corner_edge_sum_max(state, is_3on3=True):
    corners = 0
    edges = 0
    if is_3on3:
        cube = state.cube
        for i in range(18):
            if i % 3 == 0 or i % 3 == 2:
                corners = corners + manhattan_distance(cube, i, 0, True) + manhattan_distance(cube, i, 2, True)
                edges = edges + manhattan_distance(cube, i, 1, False)
            else:
                edges = edges + manhattan_distance(cube, i, 0, False) + manhattan_distance(cube, i, 2, False)
        return max(corners / 12, edges / 8)
    else:
        centers = 0
        for i in range(24):
            if i % 4 == 0 or i % 4 == 3:
                corners = corners + manhattan_distance(state, i, 0, True, False) + \
                          manhattan_distance(state, i, 3, True, False)
                edges = edges + manhattan_distance(state, i, 1, False, False) + manhattan_distance(state, i, 2, False, False)
            else:
                if i % 4 == 1:
                    edges = edges + manhattan_distance(state, i, 0, False, False) + manhattan_distance(state, i + 1, 0, False, False)
                    centers = centers + manhattan_distance_center(state, i, 1) + manhattan_distance_center(state, i, 2)
                else:
                    manhattan_distance(state, i, 3, False, False) +  manhattan_distance(state, i + 1, 3, False, False)
                    centers = centers + manhattan_distance_center(state, i, 1) + manhattan_distance_center(state, i, 2)
        return max((corners + centers) / 16, (edges + centers) / 16)


def kurf_h(state, is_3on3=True):
    corners = 0
    edges_1 = 0
    edges_2 = 0
    if is_3on3:
        cube = state.cube
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
        return max(corners / 8, edges_1 / 8, edges_2 / 8)
    else:
        centers = 0
        for i in range(24):
            if i % 4 == 0 or i % 4 == 3:
                corners = corners + manhattan_distance(state, i, 0, True, False) + manhattan_distance(state, i, 3, True,
                                                                                                     False)
                if i % 4 == 0:
                    edges_1 = edges_1 + manhattan_distance(state, i, 1, False, False) + manhattan_distance(state, i, 2, False, False)
                else:
                    edges_2 = edges_2 + manhattan_distance(state, i, 1, False, False) + manhattan_distance(state, i, 2, False, False)
            else:
                if i % 4 == 1:
                    edges_1 = edges_1 + manhattan_distance(state, i, 0, False, False) + manhattan_distance(state, i, 3, False, False)
                    centers = centers + manhattan_distance_center(state, i, 1) + manhattan_distance_center(state, i, 2)
                else:
                    edges_2 = edges_2 + manhattan_distance(state, i, 0, False, False) + manhattan_distance(state, i, 3, False, False)
                    centers = centers + manhattan_distance_center(state, i, 1) + manhattan_distance_center(state, i, 2)
        return max((corners + centers) / 16, (edges_1 + centers) / 16, (edges_2 + centers) / 16)


def sum_divided_by_eight(state, is_3on3=True):
    corners = 0
    edges = 0
    if is_3on3:
        cube = state.cube
        for i in range(18):
            if i % 3 == 0 or i % 3 == 2:
                corners = corners + manhattan_distance(cube, i, 0, True) + manhattan_distance(cube, i, 2, True)
                edges = edges + manhattan_distance(cube, i, 1, False)
            else:
                edges = edges + manhattan_distance(cube, i, 0, False) + manhattan_distance(cube, i, 2, False)
        return (corners + edges) / 8
    else:
        centers = 0
        for i in range(24):
            if i % 4 == 0 or i % 4 == 3:
                corners = corners + manhattan_distance(state, i, 0, True, False) + \
                          manhattan_distance(state, i, 3, True, False)
                edges = edges + manhattan_distance(state, i, 1, False, False) + manhattan_distance(state, i, 2, False, False)
            else:
                if i % 4 == 1:
                    edges = edges + manhattan_distance(state, i, 0, False, False) + manhattan_distance(state, i, 3, False, False)
                    centers = centers + manhattan_distance_center(state, i, 1) + manhattan_distance_center(state, i, 2)
                else:
                    edges = edges + manhattan_distance(state, i, 0, False, False) + manhattan_distance(state, i, 3, False, False)
                    centers = centers + manhattan_distance_center(state, i, 1) + manhattan_distance_center(state, i, 2)
        return (corners + edges + centers) / 16


def color_heuristic(cube, is3on3=True):
    """
    count the number of colors that different with goal.
    sometimes return non optimal solution
    """
    base_colors = ['W', 'B', 'R', 'G', 'O', 'Y']
    count = 0
    cube = cube.cube
    for i in range(6):
        if not is3on3:
            color = base_colors[i]
        else:
            color = cube[i*cube_size+1][1]

        for j in range(cube_size):
            for k in range(cube_size):
                if cube[i*cube_size+j][k] != color:
                    count += 1
    return count / (2*cube_size+2)


def ida_solve_cube(curr, heuristic=sum_divided_by_eight):
    time.ctime()
    fmt = '%H:%M:%S'
    start = time.strftime(fmt)
    if cube_size == 4:
        path_to_solution, expended_nodes = ida(curr, heuristic, False)
    else:
        path_to_solution, expended_nodes = ida(curr, heuristic)

    path_for_gui = translate_path_for_gui(path_to_solution)
    print("path to solution", path_to_solution)
    time.ctime()
    end = time.strftime(fmt)
    print("Calculation time(sec):", datetime.strptime(end, fmt) - datetime.strptime(start, fmt))
    return path_for_gui[::-1], expended_nodes


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


cube_array_4 = np.array([
    # W 0
    [[0, 0, 3], [1, 0, 3], [2, 0, 3], [3, 0, 3]],  # 2 corners + 2 edge
    [[0, 0, 2], [1, 0, 2], [2, 0, 2], [3, 0, 2]],  # 2 center + 2 edge
    [[0, 0, 1], [1, 0, 1], [2, 0, 1], [3, 0, 1]],  # 2 center + 2 edge
    [[0, 0, 0], [1, 0, 0], [2, 0, 0], [3, 0, 0]],  # 2 corners + 2 edge
    # B 4
    [[0, 0, 3], [0, 1, 3], [2, 2, 3], [3, 3, 3]],  # 2 corners + 2 edge
    [[0, 0, 2], [0, 1, 2], [2, 2, 2], [3, 3, 2]],  # 2 center + 2 edge
    [[0, 0, 1], [0, 1, 1], [2, 2, 1], [3, 3, 1]],  # center + 2 edge
    [[0, 0, 0], [0, 1, 0], [2, 2, 0], [3, 3, 0]],  # 2 corners + 2 edge
    # R 8
    [[0, 0, 0], [1, 0, 0], [2, 0, 0], [3, 0, 0]],  # 2 corners + 2 edge
    [[0, 1, 0], [1, 1, 0], [2, 1, 0], [3, 1, 0]],  # 2 center + 2 edge
    [[0, 2, 0], [1, 2, 0], [2, 2, 0], [3, 2, 0]],  # 2 center + 2 edge
    [[0, 3, 0], [1, 3, 0], [2, 3, 0], [3, 3, 0]],  # 2 corners + 2 edge
    # G 12
    [[3, 0, 0], [3, 0, 1], [3, 0, 2], [3, 0, 3]],  # 2 corners + 2 edge
    [[3, 1, 0], [3, 1, 1], [3, 1, 2], [3, 1, 3]],  # 2 center + 2 edge
    [[3, 2, 0], [3, 2, 1], [3, 2, 2], [3, 2, 3]],  # 2 center + 2 edge
    [[3, 3, 0], [3, 3, 1], [3, 3, 2], [3, 3, 3]],  # 2 corners + 2 edge
    # O 16
    [[3, 0, 3], [2, 0, 3], [1, 0, 3], [0, 0, 3]],  # 2 corners + 2 edge
    [[3, 1, 3], [2, 1, 3], [1, 1, 3], [0, 1, 3]],  # 2 center + 2 edge
    [[3, 2, 3], [2, 2, 3], [1, 2, 3], [0, 2, 3]],  # 2 center + 2 edge
    [[3, 3, 3], [2, 3, 3], [1, 3, 3], [0, 3, 3]],  # 2 corners + 2 edge
    # Y 20
    [[0, 3, 0], [1, 3, 0], [2, 3, 0], [3, 3, 0]],  # 2 corners + 2 edge
    [[0, 3, 1], [1, 3, 1], [2, 3, 1], [3, 3, 1]],  # 2 center + 2 edge
    [[0, 3, 2], [1, 3, 2], [2, 3, 2], [3, 3, 2]],  # 2 center + 2 edge
    [[0, 3, 3], [1, 3, 3], [2, 3, 3], [3, 3, 3]],  # 2 corners + 2 edge
])
run_without_gui(5)