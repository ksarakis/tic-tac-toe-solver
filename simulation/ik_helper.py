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



# NOT USED

def x_writer(robot_chain, center, side_length=0.03, z_draw=0.05, z_lift=0.1):

    half = side_length / 2.0
    cx, cy = center

    waypoints = [
        [cx + half, cy + half, z_lift],  # Top-Left
        [cx + half, cy + half, z_draw],  # Top-Left
        [cx - half, cy - half, z_draw],  # Bottom-Right
        [cx - half, cy - half, z_lift],  # Lift pen

        [cx + half, cy - half, z_lift],  # Top-Right
        [cx + half, cy - half, z_draw],  # Top-Right
        [cx - half, cy + half, z_draw],  # Bottom-Left
        [cx - half, cy + half, z_lift],  # Lift pen
    ]
    joint_configs = []
    for pt in waypoints:
        ik_sol = robot_chain.inverse_kinematics(pt, orientation_mode="Z", target_orientation=[0, 0, -1])
        joint_configs.append(ik_to_config(ik_sol, gripper=0.0))

    return joint_configs
