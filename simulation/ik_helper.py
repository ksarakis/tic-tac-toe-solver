import numpy as np

def ik_to_config(ik_solution, gripper = 0):
    return {
        "shoulder_pan":  float(np.rad2deg(ik_solution[1])),
        "shoulder_lift": float(np.rad2deg(ik_solution[2])),
        "elbow_flex":    float(np.rad2deg(ik_solution[3])),
        "wrist_flex":    float(np.rad2deg(ik_solution[4])),
        "wrist_roll":    float(np.rad2deg(ik_solution[5])),
        "gripper":       gripper,  # Explicit gripper angle (0 = closed, 100 = open)
    }

def x_writer(robot_chain, z_draw, z_lift):

    # Sequence: Stroke 1 -> Lift -> Reposition -> Touchdown -> Stroke 2
    waypoints = [
        [0.30,  0.08, z_draw],  # Up-left
        [0.20, -0.08, z_draw],  # Bottom-right
        [0.20, -0.08, z_lift],  # Lift pen
        [0.30, -0.08, z_lift],  # Above top-right
        [0.30, -0.08, z_draw],  # Lower to top-right
        [0.20,  0.08, z_draw],  # Bottom-left
        [0.20,  0.08, z_lift],  # Lift pen
    ]

    joint_configs = []
    for pt in waypoints:
        ik_sol = robot_chain.inverse_kinematics(pt)
        joint_configs.append(ik_to_config(ik_sol, gripper=0.0))

    return joint_configs
