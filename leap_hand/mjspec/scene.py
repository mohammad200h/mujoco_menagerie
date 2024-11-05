from hand import create_hand
import json
import mujoco as mj


if __name__ == "__main__":

  asset_path = "../assets/"
  leap_data_file = "./leap.json"

  with open(leap_data_file, 'r') as file:
    leap_data = json.load(file)

  model = create_hand(leap_data,asset_path)

  data = mj.MjData(model)

  # visualization
  with mj.viewer.launch_passive(
        model=model, data=data, show_left_ui=False, show_right_ui=False
    ) as viewer:
        mj.mjv_defaultFreeCamera(model, viewer.cam)

        mj.mj_forward(model, data)

        while viewer.is_running():
            mj.mj_step(model, data)
            viewer.sync()
