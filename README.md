# Tic Tac Toe solver with SO-ARM 101

**Note:** *Project under active development.*

## Current status

- Achieved satisfying recognition of the board and the noughts and crosses.

- Working IK solver(`ikpy`) both in real life and in simulation.

- Noticed small discrepancy between theoritical and real `[0, 0, 0, 0, 0, 0]`. Need to calibrate again and/or add angle offsets. 

- Implemented tic-tac-toe solver.

**To do:**


- Design and 3d-print(or find any other solution) a camera stand

- Test pick-and-place routine for game items.

- Piece all of these together.


This repository contains my try to create a simple tic tac toe solver with a SO-ARM 101. 

## Problems faced

In the first place, I wanted the arm to play the game drawing Xs and Os. However, I found out that there is no much friction between the end-effector and a pen/pencil, therefore I switched to the current implementation.

Moreover, due to limited FK and IK derivation knowledge, I didn't solve myself neither of the problems. 

When experimenting with IKpy at first, I found it difficult to control the orientation of the end effector, but after searching documentation, I found out how to do it. 

After 3d-printing Xs and Os, I found out that the current vision solution was not working at all. So, I experimented with other ways of classifying cells. The current one takes each cell, ANDs it with a simple circle, extract its contours and finds if there is a hole in the shape. If yes, it surely is a O, since X does not contain any holes in its shape. The AND operation was inserted because a simple search in contours for holes could create false positives from the shades. 

## Project structure

This project contains 3 main folders:
- `hardware\` includes all scripts meant to run in the physical manipulator

- `simulation` includes all scripts and the needed files(e.g. the `.urdf` of the arm) to run a simulation in MuJoCo in order to test inverse kinematics solvers and routines. 

- To be added: `stl` contains the `.stl` files used to 3D-print the Xs and Os.

## The board

The board is drawn on a plain A4 paper.
There are 3 yellow boxes in three out of the four corners in order to help computer vision pipeline recognise and align with the board. No vertical and horizontal lines are drawn in the board.


## Credits

The robotic arm used in this project is [SO-ARM 101](https://github.com/TheRobotStudio/SO-ARM100) by RobotStudio and HuggingFace. 

All MuJoCo and IRL scripts are based on [Maegan Tucker's lab notes](https://maegantucker.com/ECE4560/so101/) from the GeorgiaTech course *"Introduction to Robotics and Automation"*.
