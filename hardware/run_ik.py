import time
import so101_utils
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "simulation"))
from ik_helper import ik_to_config
import ikpy.chain

MOVE_TIME = 1.5
HOLD_TIME = 2.0

PORT_ID = "/dev/ttyACM0"
ROBOT_NAME = "follower-1"

robot_chain = ikpy.chain.Chain.from_urdf_file(
    "../simulation/model/so101_new_calib.urdf",
    base_elements=["base_link"],
    last_link_vector=None,
    active_links_mask=[False, True, True, True, True, True, False]  # base, 5 arm joints, gripper
)

bus = so101_utils.setup(PORT_ID, ROBOT_NAME)

starting_position = bus.sync_read("Present_Position")
print(f"Starting position: {starting_position}")

##



##

so101_utils.move_to_pose(bus, starting_position, MOVE_TIME)

time.sleep(HOLD_TIME)

bus.disable_torque()