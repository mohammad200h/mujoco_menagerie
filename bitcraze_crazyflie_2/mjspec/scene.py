
from cf2 import create_cf2
import json
import mujoco as mj

if __name__ == "__main__":

  asset_path = "../assets/"
  data_file = "./cf2.json"

  with open(data_file, 'r') as file:
    data = json.load(file)

  model = create_cf2(data,asset_path)

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