# Rubik Cube - AI project


To run the project there are 2 options:
1. run in the printed version (recommended)
2. run the GUI version.

to change the size of the cube, change the "cube_size" parameter in cube_utils.py to 
the chosen size. default is 3.

## option 1: printed version:
In cube_solve_ida.py file, run the "run_without_gui(number_of_scrambles=6, from_file=None)"  function.

you can change the number_of_scrambles for the cube. this function create scrambled cube, and than solve
the cube by thr different methods: IDA* with several heuristics, reinforcement learning, group theory.
all the relevant data and the comparison between the methods will be printed on the screen.

Have fun! 


## option 2: GUI
run the cube_interactive.py file
press "create cube" button to scramble the cube.
press "solve cube" button to solve the cube using IDA.

##### Important note 1
In order to run the GUI properly,
the project must be run through the debugger with a debugging point in the file "cube_interactive",
inside the function "_create_problem_cube" (in the first row).
##### Important note 2
the 4*4 cube solved only by the printed version.

## files in the projects:
- cube_solve_ida.py - Main file, create the rubik's cube and solve it.
- cube_utils.py - Organizes all the utilities of the cube - the structure of the cube, actions, etc. 
- group_theory_solution.py - group theory solution implementation. 
- reinforcement_learning_learner.py
- reinforcement_learning_solver.py
- weights.h5 - weights of the RL solution after learning.
- cube_interactive.py - GUI
- projection.py - GUI helper
- plot_results.py - create graphs for results
- input1.txt, output.txt - files for input and output of the gui.