import time
import mujoco
import mujoco.viewer
import numpy as np

from so101_mujoco_utils import (
    set_initial_pose,
    send_position_command,
    move_to_pose,
    hold_position,
)

from ik_helper import (
    ik_to_config,
    x_writer,
)

import ikpy.chain

robot_chain = ikpy.chain.Chain.from_urdf_file(
    "model/so101_new_calib.urdf",
    base_elements=["base_link"],
    last_link_vector=None,
    active_links_mask=[False, True, True, True, True, True, False]  # base, 5 arm joints, gripper
)

# 2. Setup MuJoCo model & data
m = mujoco.MjModel.from_xml_path("model/scene.xml")
d = mujoco.MjData(m)

def show_cube(viewer, position, orientation, geom_num=0, halfwidth=0.013):
    mujoco.mjv_initGeom(
        viewer.user_scn.geoms[geom_num],
        type=mujoco.mjtGeom.mjGEOM_BOX,
        size=[halfwidth, halfwidth, halfwidth],
        pos=position,
        mat=orientation.flatten(),
        rgba=[1, 0, 0, 0.4],
    )
    viewer.user_scn.ngeom = 1
    viewer.sync()

# 3. Initial robot joint configuration (degrees / gripper scale)
initial_config = {
    "shoulder_pan": 0.0,
    "shoulder_lift": 0.0,
    "elbow_flex": 0.0,
    "wrist_flex": 0.0,
    "wrist_roll": 0.0,
    "gripper": 0.0,
}

set_initial_pose(d, initial_config)
send_position_command(d, initial_config)

# 5. Run simulation
with mujoco.viewer.launch_passive(m, d) as viewer:
    # show_cube(viewer, desired_pose, np.eye(3))
    
    configs = x_writer(robot_chain, center=[0.1, 0.1])

    for config in configs:
        move_to_pose(m, d, viewer, config, 2.0)


    
    # Hold target pose
    hold_position(m, d, viewer, duration=5.0)