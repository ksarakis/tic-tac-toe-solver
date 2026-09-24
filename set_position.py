import time
import so101_utils

PORT_ID = "/dev/ttyACM0"
ROBOT_NAME = "follower-1"

DESIRED_POSITION = {
    "shoulder_pan": 0,
    "shoulder_lift": 0,
    "elbow_flex": 0,
    "wrist_flex": 72.57,
    "wrist_roll": -5.58,
    "gripper": 50,
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