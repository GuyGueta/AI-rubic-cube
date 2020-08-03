import numpy as np
from random import randint
import pycuber as pc
from collections import Counter
from random import choice

cube_by_color = []
cube_size = 4
for color in ['W', 'B', 'R', 'G', 'O', 'Y']:
    sub_list = [color] * cube_size
    for j in range(cube_size):
        cube_by_color.append(sub_list)
basic_cube = np.array(cube_by_color)

move_dict = {"front_clockwise": ('F', 1, 0), "front_anti_clockwise": ('F', -1, 0), "up_clockwise": ('U', 1, 0),
             "up_anti_clockwise": ('U', -1, 0), "down_clockwise": ('D', 1, 0), "down_anti_clockwise": ('D', -1, 0),
             "left_clockwise": ('L', 1, 0), "left_anti_clockwise": ('L', -1, 0), "right_clockwise": ('R', 1, 0),
             "right_anti_clockwise": ('R', -1, 0), "back_clockwise": ('B', 1, 0), "back_anti_clockwise": ('B', -1, 0)}


def save_cube(f, x):
    for i in range(3):
        f.write(" "*14 + str(x[i, 0:3])+'\n')

    for m in range(3, 6):
        f.write(str(x[m, 0:3]) + " " + str(x[m+3, 0:3]) + " " + str(x[m+6, 0:3])+" "+str(x[m+9, 0:3])+'\n')

    for k in range(15, 18):
        f.write(" "*14 + str(x[k, 0:3]) + " "*7 + '\n')


def PrintCube(x):
    for i in range(3):
        print(" "*13, str(x[i, 0:3]))

    for m in range(3, 6):
        print(str(x[m, 0:3]), str(x[m + 3, 0:3]), str(x[m + 6, 0:3]), str(x[m + 9, 0:3]))

    for k in range(15, 18):
        print(" "*13, str(x[k, 0:3]), " "*5)


def print_cube_per_size(x):
    for i in range(cube_size):
        print(" "*(cube_size*4+1), str(x[i, 0:cube_size]))

    for m in range(cube_size, cube_size+cube_size):
        print(str(x[m, 0:cube_size]), str(x[m + cube_size, 0:cube_size]),
              str(x[m + 2*cube_size, 0:cube_size]), str(x[m + 3*cube_size, 0:cube_size]))

    for k in range(cube_size*5, cube_size*6):
        print(" "*(cube_size*4+1), str(x[k, 0:cube_size]), " "*5)


move_per_num = {1: (('F', 1, 0), "front_clockwise"), 2: (('F', -1, 0), "front_anti_clockwise"),
                3: (('U', 1, 0), "up_clockwise"), 4: (('U', -1, 0), "up_anti_clockwise"),
                5: (('D', 1, 0), "down_clockwise"), 6: (('D', -1, 0), "down_anti_clockwise"),
                7: (('L', 1, 0), "left_clockwise"), 8: (('L', -1, 0), "left_anti_clockwise"),
                9: (('R', 1, 0), "right_clockwise"), 10: (('R', -1, 0), "right_anti_clockwise"),
                11: (('B', 1, 0), "back_clockwise"), 12: (('B', -1, 0), "back_anti_clockwise"),
                13: (('Z', 1, 0), "deep_front_clockwise"), 14: (('Z', -1, 0), "deep_front_anti_clockwise"),
                15: (('X', 1, 0), "deep_up_clockwise"), 16: (('X', -1, 0), "deep_up_anti_clockwise"),
                17: (('C', 1, 0), "deep_down_clockwise"), 18: (('C', -1, 0), "deep_down_anti_clockwise"),
                19: (('V', 1, 0), "deep_left_clockwise"), 20: (('V', -1, 0), "deep_left_anti_clockwise"),
                21: (('N', 1, 0), "deep_right_clockwise"), 22: (('N', -1, 0), "deep_right_anti_clockwise"),
                23: (('M', 1, 0), "deep_back_clockwise"), 24: (('M', -1, 0), "deep_back_anti_clockwise"),
                }


new_action__per_number = {1: 'F', 2: "F'", 3: 'U', 4: "U'", 5: 'D', 6: "D'",
                          7: 'L', 8: "L'", 9: 'R', 10: "R'", 11: 'B', 12: "B'"}  # to use the same cube as A*

action_map = {'F': 0, 'B': 1, 'U': 2, 'D': 3, 'L': 4, 'R': 5, "F'": 6, "B'": 7, "U'": 8, "D'": 9, "L'": 10, "R'": 11,
              'F2': 12, 'B2': 13, 'U2': 14, 'D2': 15, 'L2': 16, 'R2': 17, "F2'": 18, "B2'": 19, "U2'": 20, "D2'": 21,
              "L2'": 22, "R2'": 23}

action_map_small = {'F': 0, 'B': 1, 'U': 2, 'D': 3, 'L': 4, 'R': 5, "F'": 6, "B'": 7, "U'": 8, "D'": 9, "L'": 10, "R'": 11}
color_list_map = {'green': [1, 0, 0, 0, 0, 0], 'blue': [0, 1, 0, 0, 0, 0], 'yellow': [0, 0, 1, 0, 0, 0],
                  'red': [0, 0, 0, 1, 0, 0], 'orange': [0, 0, 0, 0, 1, 0], 'white': [0, 0, 0, 0, 0, 1]}


def perform_move(x, move, print_cube=False):
    """
    :param x: current cube
    :param move: move number
    :param print_cube: true if we want to print the cube
    :return: the move according to the given number
    """
    # perform the relevant action:
    action_per_move_num[move](x)
    if print_cube == 1:
        print_cube_per_size(x)

    return move_per_num[move]


def translate_path_for_gui(path):
    if cube_size == 3:

        gui_path = []
        for move in path:
            gui_path.append(move_dict[move])

        return gui_path
    return [None]

def create_cube(total_move, init_cube):
    """
    :param total_move: number of moves
    :param init_cube: the initial cube
    :return:
    """
    print_cube_per_size(init_cube)
    # PrintCube_per_size(init_cube)
    if cube_size == 4:
        randoms_num_for_moves = [randint(1, 24) for x in range(total_move)]
    else:
        randoms_num_for_moves = [randint(1, 12) for x in range(total_move)]
    print(randoms_num_for_moves)
    for num in randoms_num_for_moves:
        print(move_per_num[num][1])
    move_list = []
    for move in randoms_num_for_moves:
        move_list.append(perform_move(init_cube, move, False)[0])
    try:
        f = open("input1.txt", "w")
        save_cube(f, init_cube)

    except IOError:
        pass
    print_cube_per_size(init_cube)
    return move_list, randoms_num_for_moves

# moves:

def front_clockwise(x):
    x[2*cube_size:3*cube_size, 0:cube_size] = np.fliplr(x[2*cube_size:3*cube_size, 0:cube_size].transpose())
    temp1 = np.array(x[cube_size-1, 0:cube_size])
    temp2 = np.array(x[cube_size*3:cube_size*4, 0])
    temp3 = np.array(x[cube_size*5, 0:cube_size])
    temp4 = np.array(x[cube_size:2*cube_size, cube_size-1])
    x[cube_size-1, 0:cube_size] = np.fliplr([temp4])[0]
    x[cube_size*3:cube_size*4, 0] = temp1
    x[cube_size*5, 0:cube_size] = np.fliplr([temp2])[0]
    x[cube_size:2*cube_size, cube_size-1] = temp3


def deep_front_clockwise(x):
    temp1 = np.array(x[cube_size-2, 0:cube_size])
    temp2 = np.array(x[cube_size*3:cube_size*4, 1])
    temp3 = np.array(x[cube_size*5 + 1, 0:cube_size])
    temp4 = np.array(x[cube_size:2*cube_size, cube_size-2])
    x[cube_size-2, 0:cube_size] = np.fliplr([temp4])[0]
    x[cube_size*3:cube_size*4, 1] = temp1
    x[cube_size*5 + 1, 0:cube_size] = np.fliplr([temp2])[0]
    x[cube_size:2*cube_size, cube_size-2] = temp3


def front_anti_clockwise(x):
    for _ in range(3):
        front_clockwise(x)


def deep_front_anti_clockwise(x):
    for _ in range(3):
        deep_front_clockwise(x)


def up_cw(x):
    x[0:cube_size, 0:cube_size] = np.fliplr(x[0:cube_size, 0:cube_size].transpose())
    temp1 = np.array(x[4*cube_size, 0:cube_size])
    temp2 = np.array(x[3*cube_size, 0:cube_size])
    temp3 = np.array(x[2*cube_size, 0:cube_size])
    temp4 = np.array(x[cube_size, 0:cube_size])
    x[4*cube_size, 0:cube_size] = temp4
    x[3*cube_size, 0:cube_size] = temp1
    x[2*cube_size, 0:cube_size] = temp2
    x[cube_size, 0:cube_size] = temp3


def deep_up_cw(x):
    temp1 = np.array(x[4*cube_size + 1, 0:cube_size])
    temp2 = np.array(x[3*cube_size + 1, 0:cube_size])
    temp3 = np.array(x[2*cube_size + 1, 0:cube_size])
    temp4 = np.array(x[cube_size + 1, 0:cube_size])
    x[4*cube_size + 1, 0:cube_size] = temp4
    x[3*cube_size + 1, 0:cube_size] = temp1
    x[2*cube_size + 1, 0:cube_size] = temp2
    x[cube_size + 1, 0:cube_size] = temp3


def up_anc(x):
    for _ in range(3):
        up_cw(x)


def deep_up_anc(x):
    for _ in range(3):
        deep_up_cw(x)


def down_cw(x):
    x[cube_size*5:cube_size*6, 0:cube_size] = np.fliplr(x[cube_size*5:cube_size*6, 0:cube_size].transpose())
    temp1 = np.array(x[cube_size*3-1, 0:cube_size])
    temp2 = np.array(x[cube_size*4-1, 0:cube_size])
    temp3 = np.array(x[cube_size*5-1, 0:cube_size])
    temp4 = np.array(x[cube_size*2-1, 0:cube_size])
    x[cube_size*3-1, 0:cube_size] = temp4
    x[cube_size*4-1, 0:cube_size] = temp1
    x[cube_size*5-1, 0:cube_size] = temp2
    x[cube_size*2-1, 0:cube_size] = temp3


def deep_down_cw(x):
    temp1 = np.array(x[cube_size*3-2, 0:cube_size])
    temp2 = np.array(x[cube_size*4-2, 0:cube_size])
    temp3 = np.array(x[cube_size*5-2, 0:cube_size])
    temp4 = np.array(x[cube_size*2-2, 0:cube_size])
    x[cube_size*3-2, 0:cube_size] = temp4
    x[cube_size*4-2, 0:cube_size] = temp1
    x[cube_size*5-2, 0:cube_size] = temp2
    x[cube_size*2-2, 0:cube_size] = temp3


def down_acw(x):
    for _ in range(3):
        down_cw(x)


def deep_down_acw(x):
    for _ in range(3):
        deep_down_cw(x)


def left_cw(x):
    x[cube_size:cube_size*2, 0:cube_size] = np.fliplr(x[cube_size:cube_size*2, 0:cube_size].transpose())
    temp1 = np.array(x[0:cube_size, 0])
    temp2 = np.array(x[cube_size*2:cube_size*3, 0])
    temp3 = np.array(x[cube_size*5:cube_size*6, 0])
    temp4 = np.array(x[cube_size*4:cube_size*5, cube_size-1])
    x[0:cube_size, 0] = np.fliplr([temp4])[0]
    x[cube_size*2:cube_size*3, 0] = temp1
    x[cube_size*5:cube_size*6, 0] = temp2
    x[cube_size*4:cube_size*5, cube_size-1] = np.fliplr([temp3])[0]


def deep_left_cw(x):
    temp1 = np.array(x[0:cube_size, 1])
    temp2 = np.array(x[cube_size*2:cube_size*3, 1])
    temp3 = np.array(x[cube_size*5:cube_size*6, 1])
    temp4 = np.array(x[cube_size*4:cube_size*5, cube_size-2])
    x[0:cube_size, 1] = np.fliplr([temp4])[0]
    x[cube_size*2:cube_size*3, 1] = temp1
    x[cube_size*5:cube_size*6, 1] = temp2
    x[cube_size*4:cube_size*5, cube_size-2] = np.fliplr([temp3])[0]


def left_acw(x):
    for _ in range(3):
        left_cw(x)


def deep_left_acw(x):
    for _ in range(3):
        deep_left_cw(x)


def right_cw(x):
    x[cube_size*3:cube_size*4, 0:cube_size] = np.fliplr(x[cube_size*3:cube_size*4, 0:cube_size].transpose())
    temp1 = np.array(x[0:cube_size, cube_size-1])
    temp2 = np.array(x[cube_size*4:cube_size*5, 0])
    temp3 = np.array(x[cube_size*5:cube_size*6, cube_size-1])
    temp4 = np.array(x[cube_size*2:cube_size*3, cube_size-1])
    x[0:cube_size, cube_size-1] = temp4
    x[cube_size*4:cube_size*5, 0] = np.fliplr([temp1])[0]
    x[cube_size*5:cube_size*6, cube_size-1] = np.fliplr([temp2])[0]
    x[cube_size*2:cube_size*3, cube_size-1] = temp3


def deep_right_cw(x):
    temp1 = np.array(x[0:cube_size, cube_size-2])
    temp2 = np.array(x[cube_size*4:cube_size*5, 1])
    temp3 = np.array(x[cube_size*5:cube_size*6, cube_size-2])
    temp4 = np.array(x[cube_size*2:cube_size*3, cube_size-2])
    x[0:cube_size, cube_size-2] = temp4
    x[cube_size*4:cube_size*5, 1] = np.fliplr([temp1])[0]
    x[cube_size*5:cube_size*6, cube_size-2] = np.fliplr([temp2])[0]
    x[cube_size*2:cube_size*3, cube_size-2] = temp3


def right_acw(x):
    for _ in range(3):
        right_cw(x)


def deep_right_acw(x):
    for _ in range(3):
        deep_right_cw(x)


def back_cw(x):
    x[cube_size*4:cube_size*5, :] = np.fliplr(x[cube_size*4:cube_size*5, :].transpose())
    temp1 = np.array(x[0, 0:cube_size])
    temp2 = np.array(x[cube_size:2*cube_size, 0])
    temp3 = np.array(x[cube_size*6-1, 0:cube_size])
    temp4 = np.array(x[cube_size*3:cube_size*4, cube_size-1])
    x[0, 0:cube_size] = temp4
    x[cube_size:2*cube_size, 0] = np.fliplr([temp1])[0]
    x[cube_size*6-1, 0:cube_size] = temp2
    x[cube_size*3:cube_size*4, cube_size-1] = np.fliplr([temp3])[0]


def deep_back_cw(x):
    temp1 = np.array(x[1, 0:cube_size])
    temp2 = np.array(x[cube_size:2*cube_size, 1])
    temp3 = np.array(x[cube_size*6-2, 0:cube_size])
    temp4 = np.array(x[cube_size*3:cube_size*4, cube_size-2])
    x[1, 0:cube_size] = temp4
    x[cube_size:2*cube_size, 1] = np.fliplr([temp1])[0]
    x[cube_size*6-2, 0:cube_size] = temp2
    x[cube_size*3:cube_size*4, cube_size-2] = np.fliplr([temp3])[0]


def back_acw(x):
    for _ in range(3):
        back_cw(x)


def deep_back_acw(x):
    for _ in range(3):
        deep_back_cw(x)


action_per_move_num = {1: front_clockwise, 2: front_anti_clockwise, 3: up_cw, 4: up_anc, 5: down_cw,
                       6: down_acw, 7: left_cw, 8: left_acw, 9: right_cw, 10: right_acw, 11: back_cw,
                       12: back_acw, 13: deep_front_clockwise, 14: deep_front_anti_clockwise,
                       15: deep_up_cw, 16: deep_up_anc, 17: deep_down_cw, 18: deep_down_acw, 19: deep_left_cw,
                       20: deep_left_acw, 21: deep_right_cw, 22: deep_right_acw, 23: deep_back_cw, 24: deep_back_acw}


# helper function for the reinforcement learning:


def flatten(cube):
    sides = [cube.F, cube.B, cube.U, cube.D, cube.L, cube.R]
    flat = []
    for x in sides:
        for i in range(3):
            for j in range(3):
                flat.append(x[i][j].colour)
    return flat


def flatten_1d_b(cube):
    sides = [cube.F, cube.B, cube.U, cube.D, cube.L, cube.R]
    flat = []
    for x in sides:
        for i in range(3):
            for j in range(3):
                flat.extend(color_list_map[x[i][j].colour])
    return flat


def order(data):
    if len(data) <= 1:
        return 0

    counts = Counter()

    for d in data:
        counts[d] += 1

    probs = [float(c) / len(data) for c in counts.values()]

    return max(probs)


def perc_solved_cube(cube):
    flat = flatten(cube)
    perc_side = [order(flat[i:(i + 9)]) for i in range(0, 9 * 6, 9)]
    return np.mean(perc_side)


def gen_sample(n_steps=6):
    cube = pc.Cube()

    transformation = [choice(list(action_map.keys())) for _ in range(n_steps)]
    print(transformation)


    # todo - ^^^ this is the scramble actions. need to create a dict
    my_formula = pc.Formula(transformation)

    cube(my_formula)

    my_formula.reverse()

    sample_X = []
    sample_Y = []
    cubes = []

    for s in my_formula:
        sample_X.append(flatten_1d_b(cube))
        sample_Y.append(action_map[s.name])
        cubes.append(cube.copy())
        cube(s.name)

    return sample_X, sample_Y, cubes

# todo - i add this lines to create a cube:


def gen_sample_2(move_list, n_steps=6):
    cube = pc.Cube()
    transformation = []
    for act in move_list:
        transformation.append(new_action__per_number[act])
    # transformation = [choice(list(action_map.keys())) for _ in range(n_steps)]
    print(transformation)

    # todo - ^^^ this is the scramble actions. need to create a dict
    my_formula = pc.Formula(transformation)

    cube(my_formula)

    my_formula.reverse()

    sample_X = []
    sample_Y = []
    cubes = []

    for s in my_formula:
        sample_X.append(flatten_1d_b(cube))
        sample_Y.append(action_map[s.name])
        cubes.append(cube.copy())
        cube(s.name)

    return sample_X, sample_Y, cubes


def gen_sequence(n_steps=6):
    cube = pc.Cube()

    transformation = [choice(list(action_map_small.keys())) for _ in range(n_steps)]

    my_formula = pc.Formula(transformation)

    cube(my_formula)

    my_formula.reverse()

    cubes = []
    distance_to_solved = []

    for i, s in enumerate(my_formula):
        cubes.append(cube.copy())
        cube(s.name)
        distance_to_solved.append(n_steps-i)

    return cubes, distance_to_solved


def get_all_possible_actions_cube_small(cube):

    flat_cubes = []
    rewards = []

    for a in action_map_small:
        cube_copy = cube.copy()
        cube_copy = cube_copy(a)
        flat_cubes.append(flatten_1d_b(cube_copy))
        rewards.append(2*int(perc_solved_cube(cube_copy)>0.99)-1)

    return flat_cubes, rewards

def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))