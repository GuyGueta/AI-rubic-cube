from rubik_solver import utils
from rubik_solver.Cubie import Cubie

from cube_interactive import *

# str_cube_example = 'wowgybwyogygybyoggrowbrgywrborwggybrbwororbwborgowryby'
# 3 solvers for the cube: 'Beginner', 'CFOP', 'Kociemba'. To solve use - utils.solve(str_cube_example, 'Kociemba')

# back_indices = [0, 3, 6, 1, 4, 7, 2, 5, 8]
# front_indices = [45, 48, 51, 46, 49, 52, 47, 50, 53]
# left_indices = [17, 14, 11, 16, 13, 10, 15, 12, 9]
# right_indices = [33, 30, 27, 34, 31, 28, 35, 32, 29]
# down_indices = [24, 21, 18, 25, 22, 19, 26, 23, 20]
# up_indices = [44, 41, 38, 43, 40, 37, 42, 39, 36]

group_theory_q_learn_mapping_dict = {(-1, -1, 1): (6, 11, 18), (-1, 0, 1): (3, 10, -1), (-1, 1, 1): (0, 9, 38),
                                     (0, -1, 1): (7, -1, 19), (0, 0, 1): (4, -1, -1), (0, 1, 1): (1, -1, 37),
                                     (1, -1, 1): (8, 27, 20), (1, 0, 1): (5, 28, -1), (1, 1, 1): (2, 29, 36),
                                     (-1, -1, -1): (45, 17, 24), (-1, -1, 0): (-1, 14, 21), (0, -1, -1): (46, -1, 25),
                                     (0, -1, 0): (-1, -1, 22), (1, -1, -1): (47, 33, 26), (1, -1, 0): (-1, 30, 23),
                                     (-1, 0, -1): (48, 16, -1), (-1, 1, -1): (51, 15, 44), (0, 0, -1): (49, -1, -1),
                                     (0, 1, -1): (52, -1, 43), (1, 0, -1): (50, 34, -1), (1, 1, -1): (53, 35, 42),
                                     (-1, 0, 0): (-1, 13, -1), (-1, 1, 0): (-1, 12, 41), (1, 0, 0): (-1, 31, -1),
                                     (1, 1, 0): (-1, 32, 39), (0, 1, 0): (-1, 40, -1)
                                     }


def from_str_to_cubie(cube_str):
    cube_list = [char for char in cube_str]
    cube_list.append(None)
    cube = []
    for i in range(3):
        for j in range(3):
            for k in range(3):
                if i == 1 and j == 1 and k == 1:
                    continue
                FB_color_idx, LR_color_idx, UD_color_idx = group_theory_q_learn_mapping_dict[(i - 1, j - 1, k - 1)]
                FB_color, LR_color, UD_color = cube_list[FB_color_idx], cube_list[LR_color_idx], cube_list[UD_color_idx]
                if FB_color is not None:
                    FB_color = FB_color.upper()
                if LR_color is not None:
                    LR_color = LR_color.upper()
                if UD_color is not None:
                    UD_color = UD_color.upper()
                cube.append(Cubie(i - 1, j - 1, k - 1, FB_color, UD_color, LR_color))
    return State(3, cube)


def from_cube_to_str(cube):
    cube_str_lst = 55 * [None]
    for cubie in cube.cube:
        x, y, z, FB_color, LR_color, UD_color = cubie.x, cubie.y, cubie.z, cubie.FB_color, cubie.LR_color, cubie.UD_color
        FB_color_idx, LR_color_idx, UD_color_idx = group_theory_q_learn_mapping_dict[(x, y, z)]
        cube_str_lst[FB_color_idx] = FB_color
        cube_str_lst[LR_color_idx] = LR_color
        cube_str_lst[UD_color_idx] = UD_color
    cube_str_lst = cube_str_lst[0:-1]
    cube_str = "".join(cube_str_lst).lower()
    return cube_str


def actions_from_group_theory_to_q_learn(group_theory_actions):
    q_learn_actions = []
    for action in group_theory_actions:
        direction = action.face
        if action.clockwise:
            clockwise = 1
        else:
            clockwise = -1
        if action.double:
            number_of_steps = 2
        else:
            number_of_steps = 1
        q_learn_actions.append((direction, clockwise * number_of_steps, 0))
    return q_learn_actions


def solve_with_group_theory(cube):
    return actions_from_group_theory_to_q_learn(utils.solve(from_cube_to_str(cube), 'Kociemba'))


print(from_str_to_cubie('wowgybwyogygybyoggrowbrgywrborwggybrbwororbwborgowryby'))
print(utils.solve('wowgybwyogygybyoggrowbrgywrborwggybrbwororbwborgowryby', 'Kociemba'))