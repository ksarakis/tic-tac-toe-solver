# Tic Tac Toe solver with SO-ARM 101

**Note:** *Project under active development.*

## Current status

- Achieved satisfying recognition of the board and the noughts and crosses.

- Working IK solver(`ikpy`) both in real life and in simulation.

**To do:**

- Design and 3d-print noughts and crosses.

- Design and 3d-print(or find any other solution) a camera stand

- Test pick-and-place routine for game items.

- Implement a solver for tic-tac-toe(possible algorithm: mini-max)

- Piece all of these together.


This repository contains my try to create a simple tic tac toe solver with a SO-ARM 101. 

## Problems faced

In the first place, I wanted the arm to play the game drawing Xs and Os. However, I found out that there is no much friction between the end-effector and a pen/pencil, therefore I switched to the current implementation.

Moreover, due to limited FK and IK derivation knowledge, I didn't solve myself neither of the problems. 

When experimenting with IKpy at first, I found it difficult to control the orientation of the end effector, but after searching documentation, I found out how to do it. 

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

All MuJoCo and IRL scripts are based on Maegan Tucker's lab notes from the GeorgiaTech course *"Introduction to Robotics and Automation"*.
