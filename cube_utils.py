import numpy as np
from random import randint


cube_by_color = []
cube_size = 3
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

# def PrintCube_per_size(x):
#     cube_size = 4
#     for i in range(cube_size):
#         print(" "*17, str(x[i, 0:cube_size]))
#
#     for m in range(cube_size, cube_size+cube_size):
#         print(str(x[m, 0:cube_size]), str(x[m + cube_size, 0:cube_size]),
#               str(x[m + 2*cube_size, 0:cube_size]), str(x[m + 3*cube_size, 0:cube_size]))
#
#     for k in range(20, 24):
#         print(" "*17, str(x[k, 0:cube_size]), " "*5)


move_per_num = {1: (('F', 1, 0), "front_clockwise"), 2: (('F', -1, 0), "front_anti_clockwise"),
                3: (('U', 1, 0), "up_clockwise"), 4: (('U', -1, 0), "up_anti_clockwise"),
                5: (('D', 1, 0), "down_clockwise"), 6: (('D', -1, 0), "down_anti_clockwise"),
                7: (('L', 1, 0), "left_clockwise"), 8: (('L', -1, 0), "left_anti_clockwise"),
                9: (('R', 1, 0), "right_clockwise"), 10: (('R', -1, 0), "right_anti_clockwise"),
                11: (('B', 1, 0), "back_clockwise"), 12: (('B', -1, 0), "back_anti_clockwise")}


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
        PrintCube(x)

    return move_per_num[move]


def translate_path_for_gui(path):
    gui_path = []
    for move in path:
        gui_path.append(move_dict[move])

    return gui_path


def create_cube(total_move, init_cube):
    """
    :param total_move: number of moves
    :param init_cube: the initial cube
    :return:
    """
    PrintCube(init_cube)
    # PrintCube_per_size(init_cube)
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
    PrintCube(init_cube)
    return move_list


# moves:

def front_clockwise(x):
    x[6:9, 0:3] = np.fliplr(x[6:9, 0:3].transpose())
    temp1 = np.array(x[2, 0:3])
    temp2 = np.array(x[9:12, 0])
    temp3 = np.array(x[15, 0:3])
    temp4 = np.array(x[3:6, 2])
    x[2, 0:3] = np.fliplr([temp4])[0]
    x[9:12, 0] = temp1
    x[15, 0:3] = np.fliplr([temp2])[0]
    x[3:6, 2] = temp3


def front_anti_clockwise(x):
    for _ in range(3):
        front_clockwise(x)


def up_cw(x):
    x[0:3, 0:3] = np.fliplr(x[0:3, 0:3].transpose())
    temp1 = np.array(x[12, 0:3])
    temp2 = np.array(x[9, 0:3])
    temp3 = np.array(x[6, 0:3])
    temp4 = np.array(x[3, 0:3])
    x[12, 0:3] = temp4
    x[9, 0:3] = temp1
    x[6, 0:3] = temp2
    x[3, 0:3] = temp3


def up_anc(x):
    for _ in range(3):
        up_cw(x)


def down_cw(x):
    x[15:18, 0:3] = np.fliplr(x[15:18, 0:3].transpose())
    temp1 = np.array(x[8, 0:3])
    temp2 = np.array(x[11, 0:3])
    temp3 = np.array(x[14, 0:3])
    temp4 = np.array(x[5,0:3])
    x[8, 0:3] = temp4
    x[11, 0:3] = temp1
    x[14, 0:3] = temp2
    x[5, 0:3] = temp3


def down_acw(x):
    for _ in range(3):
        down_cw(x)


def left_cw(x):
    x[3:6, 0:3] = np.fliplr(x[3:6, 0:3].transpose())
    temp1 = np.array(x[0:3, 0])
    temp2 = np.array(x[6:9, 0])
    temp3 = np.array(x[15:18, 0])
    temp4 = np.array(x[12:15, 2])
    x[0:3, 0] = np.fliplr([temp4])[0]
    x[6:9, 0] = temp1
    x[15:18, 0] = temp2
    x[12:15, 2] = np.fliplr([temp3])[0]


def left_acw(x):
    for _ in range(3):
        left_cw(x)


def right_cw(x):
    x[9:12, 0:3] = np.fliplr(x[9:12, 0:3].transpose())
    temp1 = np.array(x[0:3, 2])
    temp2 = np.array(x[12:15, 0])
    temp3 = np.array(x[15:18, 2])
    temp4 = np.array(x[6:9, 2])
    x[0:3, 2] = temp4
    x[12:15, 0] = np.fliplr([temp1])[0]
    x[15:18, 2] = np.fliplr([temp2])[0]
    x[6:9, 2] = temp3


def right_acw(x):
    for _ in range(3):
        right_cw(x)


def back_cw(x):
    x[12:15, :] = np.fliplr(x[12:15, :].transpose())
    temp1 = np.array(x[0, 0:3])
    temp2 = np.array(x[3:6, 0])
    temp3 = np.array(x[17, 0:3])
    temp4 = np.array(x[9:12, 2])
    x[0, 0:3] = temp4
    x[3:6, 0] = np.fliplr([temp1])[0]
    x[17, 0:3] = temp2
    x[9:12, 2] = np.fliplr([temp3])[0]


def back_acw(x):
    for _ in range(3):
        back_cw(x)


action_per_move_num = {1: front_clockwise, 2: front_anti_clockwise, 3: up_cw, 4: up_anc, 5: down_cw,
                       6: down_acw, 7: left_cw, 8: left_acw, 9: right_cw, 10: right_acw, 11: back_cw,
                       12: back_acw}
