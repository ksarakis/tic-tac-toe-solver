import time
import mujoco
import mujoco.viewer
from so101_mujoco_utils import set_initial_pose, send_position_command, \
    convert_to_dictionary, convert_to_list, move_to_pose, hold_position

m = mujoco.MjModel.from_xml_path('model/scene.xml')
d = mujoco.MjData(m)

starting_position = [0.0, -1.57, 1.55, 0.846, 0.0, 0.0]  # in rads and gripper in 0-100 range

desired_position = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]  # in rads and gripper in 0-100 range

set_initial_pose(d, convert_to_dictionary(starting_position))

with mujoco.viewer.launch_passive(m, d) as viewer:
  # Close the viewer automatically after 30 wall-seconds.
  start = time.time()
  while viewer.is_running() and time.time() - start < 30:
    step_start = time.time()


    move_to_pose(m, d, viewer, convert_to_dictionary(desired_position), duration=2.0)
    hold_duration = 2.0  # seconds
    hold_position(m, d, viewer, hold_duration)
    move_to_pose(m, d, viewer, convert_to_dictionary(starting_position), duration=2.0)

    # mj_step can be replaced with code that also evaluates
    # a policy and applies a control signal before stepping the physics.
    mujoco.mj_step(m, d)

    # Pick up changes to the physics state, apply perturbations, update options from GUI.
    viewer.sync()

    # Rudimentary time keeping, will drift relative to wall clock.
    time_until_next_step = m.opt.timestep - (time.time() - step_start)
    if time_until_next_step > 0:
      time.sleep(time_until_next_step)
