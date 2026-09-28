import time
# import so101_utils
from ik_helper import (
    ik_to_config,
    x_writer,
)

import ikpy.chain

robot_chain = ikpy.chain.Chain.from_urdf_file(
    "../simulation/model/so101_new_calib.urdf",
    base_elements=["base_link"],
    last_link_vector=None,
    active_links_mask=[False, True, True, True, True, True, False]  # base, 5 arm joints, gripper
)

PORT_ID = "/dev/ttyACM0"
ROBOT_NAME = "follower-1"

DESIRED_POSITION = {
    "shoulder_pan": 0.0,
    "shoulder_lift": 0.0,
    "elbow_flex": 0.0,
    "wrist_flex": 0.0,
    "wrist_roll": 0.0,
    "gripper": 50.0,
}

MOVE_TIME = 4.0
HOLD_TIME = 2.0

bus = so101_utils.setup(PORT_ID, ROBOT_NAME)

starting_position = bus.sync_read("Present_Position")
print(f"Starting position: {starting_position}")

so101_utils.move_to_pose(bus, DESIRED_POSITION, MOVE_TIME)

time.sleep(HOLD_TIME)

so101_utils.move_to_pose(bus, starting_position, MOVE_TIME)

time.sleep(HOLD_TIME)

bus.disable_torque()